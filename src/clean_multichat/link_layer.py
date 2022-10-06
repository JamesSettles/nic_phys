import physical_layer as nic
import time
import text_to_binary as t2bin
"""
Link layer should only deal with sending and receiving packets of data across machine
"""
class Packet:
    """
    A packet of data sent from one machine to the other.
    Each packet starts with a 1 and ends with a 0
    Each packet of data contains 3 bits specifying the port number that the packet
    came from
    Each packet contains 1 parity bit to ensure the port number is sent correctly. This prevents duplicate 
    msg's from being sent from other ports
    Each packet contains 4 length bits that specify the length of the actual msg
    Each packet contains up to 15 msg bits
    """
    def __init__(self, bin_msg: str, port: int):
        self.port_header = None # 3 bits for port num one parity bit
        self.parity_bit = None
        self.length_header = None # length header specifies length of binary message
        self.bin_msg = bin_msg
        # Gets the binary encoding of bin_rep_size of an integer  
        int_to_binary = lambda integer, bin_rep_size: format(integer, "b").zfill(bin_rep_size)
        self.port_header = int_to_binary(port,3)
        self.parity_bit = "1" if self.port_header.count("1") % 2 else "0"
        # Encoding of escape character
        if bin_msg == None:
            self.total_bit_pattern = "1" + self.port_header + self.parity_bit + "0000"
        else:
            self.length_header = int_to_binary(len(bin_msg),4)
            self.total_bit_pattern = "0" + self.port_header + self.parity_bit + self.length_header + bin_msg + "0"
"""
Sends a bit pattern across a port bit by bit
"""
def send_bit_pattern(port: str, bit_pattern: str, bit_width: int):
    print(f"Sending bit msg: {bit_pattern}")
    new_packet = Packet(bit_pattern, port)
    print(f"Total bit pattern sent: {new_packet.total_bit_pattern}")
    for bit in new_packet.total_bit_pattern:
        nic.nic_send_on_port(bit, port)
        time.sleep(bit_width)
"""
Waits for a message to be sent then returns the bit pattern on the sent msg
"""
def receive_bit_message(port:int, bit_width:int):
    # keep checking for start of a msg "1" on given port
    while nic.nic_recv_from_port(port) == "0":  
        continue
    return read_in_packet(port,bit_width)
"""
Reads in the length header and bit msg being transmitted across a given port
"""
def read_in_bit_msg(port: int , bit_width:int) -> str:
    # read in header size
    length_header = ""
    bit_msg = ""
    for bit in range(4): # read in heaider bits
        length_header += nic.nic_recv_from_port(port)
        time.sleep(bit_width)
    length_header_as_int = int(length_header,2) # convert length header to int
    # check for escape character
    if length_header_as_int == 0:
        return None
    for bit in range(length_header_as_int):
        bit_msg += nic.nic_recv_from_port(port)
        time.sleep(bit_width)
    return bit_msg
"""
Reads in a packet being transmitted across a given port and 
returns the bit msg sent in that packet, -1 if parity bit caught an error,
or None if an escape sequence is read
"""
def read_in_packet(port:int, bit_width:int):
    port_header = ""
    # sleep bit width and a half to get into the center of the sent bit window
    time.sleep(bit_width * 1.5)
    # read in port_header and parity bit
    for bit in range(4):
        port_header += nic.nic_recv_from_port(port)
        time.sleep(bit_width)
    # check if parity bit caught an error, if so throw the message out
    num_ones = port_header.count("1")
    if int(num_ones) % 2:
        print("Parity bit caught an error decoding port header")
        return -1
    # check to see if sent port matches up with receiving port
    if port == int(port_header[:-1], 2):
        bit_msg = read_in_bit_msg(port, bit_width)
        return bit_msg if bit_msg else None