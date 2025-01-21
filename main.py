from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4
import ipaddress

class SimpleSDNController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super(SimpleSDNController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}  # Stores MAC-to-port mappings
        self.traffic_data = {}  # Dictionary for traffic monitoring
    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Handles initial connection with a switch."""
        datapath = ev.msg.datapath
        self._install_table_miss_flow(datapath)
    
    def _install_table_miss_flow(self, datapath):
        """Install a table-miss flow entry to handle unmatched packets."""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Match all packets
        match = parser.OFPMatch()
        # Send unmatched packets to the controller
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        
        # Create a flow mod message
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        flow_mod = parser.OFPFlowMod(
            datapath=datapath, priority=0, match=match, instructions=inst
        )
        # Send the flow mod message to the switch
        datapath.send_msg(flow_mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """Handles packets that are sent to the controller."""
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Extract packet data
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        # Log the packet reception
        self.logger.info("Packet received on port %s", in_port)

        if ip_pkt:
            # Extract source and destination IP addresses
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst

            # Check if both source and destination IPs are in the same subnet (10.0.0.0/24)
            subnet = ipaddress.IPv4Network('10.0.0.0/24', strict=False)
            if ipaddress.IPv4Address(src_ip) in subnet and ipaddress.IPv4Address(dst_ip) in subnet:
                # Forward the packet if both IPs are in the same subnet
                self.logger.info(f"Forwarding packet from {src_ip} to {dst_ip}")
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
                out = parser.OFPPacketOut(
                    datapath=datapath,
                    buffer_id=msg.buffer_id,
                    in_port=in_port,
                    actions=actions,
                    data=msg.data
                )
                datapath.send_msg(out)
            else:
                # Drop the packet if the IPs are in different subnets
                self.logger.info(f"Dropping packet from {src_ip} to {dst_ip} (different subnets)")
                return

            # Update traffic data (monitor packet counts per host and port)
            self.update_traffic_data(src_ip, 'host')
            self.update_traffic_data(dst_ip, 'host')
            self.update_traffic_data(in_port, 'port')

    def update_traffic_data(self, key, entity_type):
        """Update traffic count for a host or port."""
        if key not in self.traffic_data:
            self.traffic_data[key] = 0
        self.traffic_data[key] += 1
        
        # Log traffic data periodically (for demonstration purposes)
        if entity_type == 'host':
            self.logger.info(f"Traffic for Host {key}: {self.traffic_data[key]} packets")
        elif entity_type == 'port':
            self.logger.info(f"Traffic on Port {key}: {self.traffic_data[key]} packets")
