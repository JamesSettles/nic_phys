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
def nic_send_all_ports(input_4bit_representation: str):
    pi.write(27, int(input_4bit_representation[0]))
    pi.write(25, int(input_4bit_representation[1]))
    pi.write(23, int(input_4bit_representation[2]))
    pi.write(21, int(input_4bit_representation[3]))

"""
Writes a bit to a specific port

"""
def nic_send_on_port(bit: str, port: int):
    pi.write(27 - ((port - 1) * 2), int(bit))

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
    return str(pi.read(26 - ((port - 1) * 2)))
"""
"Flushes" the ports, this can help with floating voltage problems
"""
def flush():
    nic_send_all_ports("0000")
    nic_send_all_ports("1111")
    nic_send_all_ports("0000")
