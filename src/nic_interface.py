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

# ================== send receive functions ===================

def initialize_communication(port):
    print(f"initializing communication, sending on port {port}")
    nic_port_send("0", port)
    read_value = nic_recv_from_port(port) 
    print("reading nic port values, wating for verification")
    while (read_value != "0"):
        read_value = nic_recv_from_port(port) 
        print("reading nic port values, wating for verification")
    print("verification received")
    return True

class Packet:
    """
    msg is any stringified binary, any conversions from text string -> binary
    or int -> binary should be done outside this class
    """
    def __init__(self, msg):
        self.bit_msg = msg 
        getbinary = lambda x, n: format(x, "b").zfill(n)
        self.header = getbinary(len(self.bit_msg), 4)
        self.header = "1" + self.header
        self.bit_msg = self.bit_msg + "0"
        self.total_msg = self.header + self.bit_msg

# send
def send_message(port: str, message: str, sleep_time: int):
    if message == None:
        bit_sequence = "10000" # null char has a size of 0
    else:
        new_packet = Packet(message)
        bit_sequence = new_packet.total_msg
        #print(bit_sequence)
    for bit in bit_sequence:
        nic_port_send(bit, port)
        time.sleep(sleep_time)

# reads in 12 bits
def read_bit_stream(port:int, sleep_time:int):
    time.sleep(sleep_time * 1.5)     # to get in the middle of first significant bit
    msg = [nic_recv_from_port(port)]
    for i in range(11):              # read 1 bit, max of 12 total, so read next 11
        time.sleep(sleep_time)
        msg.append(nic_recv_from_port(port))
    return msg

def receive_message(port, sleep_time):
    is_waiting_for_msg_start = True 
    while is_waiting_for_msg_start:
        if nic_recv_from_port(port) == "1":
            # starts reading in whole msg
            bits_in_msg = read_bit_stream(port, sleep_time)
            is_waiting_for_msg_start = False
    # begin processing msg
    #print(bits_in_msg)
    header_bits = "" # will be a str of the binary rep of message length
    # read bits from header
    for header_bit in bits_in_msg[:4]:
        header_bits += header_bit
        bits_in_msg.remove(header_bit)
    header_bits = int(header_bits, 2)
    if header_bits == 0:
        return None
    # reading from msg bits
    msg = ""
    for msg_bit in bits_in_msg[:header_bits]:
        msg += msg_bit
    return t2bin.bin_to_char(msg)

# zeros out the ports
def flush():
    nic_send("1111")