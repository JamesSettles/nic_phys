import pigpio
import time
import text_to_binary as t2bin
pi = pigpio.pi()   
# Port 1
pi.set_mode(27,pigpio.OUTPUT)
pi.set_mode(26, pigpio.INPUT)
# Port 2
pi.set_mode(25,pigpio.OUTPUT)
pi.set_mode(24,pigpio.INPUT)
# Port 3
pi.set_mode(23,pigpio.OUTPUT)
pi.set_mode(22,pigpio.INPUT)
# Port 4
pi.set_mode(21,pigpio.OUTPUT)
pi.set_mode(20,pigpio.INPUT)

"""
Takes in a stringified 4-bit representation of the ports to send to
"0011" would send to ports 3 & 4
"""
def nic_send(input_4bit_representation: str):
    pi.write(27, int(input_4bit_representation[0]))
    pi.write(25, int(input_4bit_representation[1]))
    pi.write(23, int(input_4bit_representation[2]))
    pi.write(21, int(input_4bit_representation[3]))

"""
Writes a bit to a specific port
"""
def nic_port_send(bit: str, port: int):
    if port == 1:
        pi.write(27, int(bit))
    if port == 2:
        pi.write(25, int(bit))
    if port == 3:
        pi.write(23, int(bit))
    else:
        pi.write(21, int(bit))

"""
Returns a stringified 4-bit value indicating the receiver states
"""
def nic_recv_all_ports() -> str:
    reciever_4bit_representation = [0,0,0,0]
    reciever_4bit_representation[0] = str(pi.read(26))
    reciever_4bit_representation[1] = str(pi.read(24))
    reciever_4bit_representation[2] = str(pi.read(22))
    reciever_4bit_representation[3] = str(pi.read(20))
    return "".join(reciever_4bit_representation) 
"""
Reads bits at given port
"""
def nic_recv_from_port(port) -> str:
    return nic_recv_all_ports()[port-1]

# zeros out the ports
def flush():
    nic_send("1111")