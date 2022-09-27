# nic_phys
Reusable code for driving the physical layer.

## Authors
- [scural](https://github.com/scural)
- [JamesSettles](https://github.com/JamesSettles)
- [RobertMusser](https://github.com/RobertMusser)

### Languages used
- Python

### SRC Directory
#### Packages Used
- pigpio 
#### nic_interface.py
Library that provides the nic_send() and nic_recv() methods. The nic_send() method takes in 4 bit value that turns on/off the transmitters on the NIC board. The nic_recv() method returns a 4 bit value that informs the user of which transmitters are on/off.

### blinky_lights.py
A simple program that provides a command line interface for interactively sending and receiving to and from the NIC