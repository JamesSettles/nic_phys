import nic_interface as nic
import time
import text_to_binary as t2bin

def initialize_communication(port):
    nic.flush()
    print(f"initializing communication, sending on port {port}")
    nic.nic_port_send("0", port)
    read_value = nic.nic_recv_from_port(port) 
    print("reading nic port values, wating for verification")
    while (read_value != "0"):
        read_value = nic.nic_recv_from_port(port) 
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
        nic.nic_port_send(bit, port)
        time.sleep(sleep_time)

# reads in 12 bits
def read_bit_stream(port:int, sleep_time:int):
    time.sleep(sleep_time * 1.5)     # to get in the middle of first significant bit
    msg = [nic.nic_recv_from_port(port)]
    for i in range(11):              # read 1 bit, max of 12 total, so read next 11
        time.sleep(sleep_time)
        msg.append(nic.nic_recv_from_port(port))
    return msg

def receive_message(port, sleep_time):
    is_waiting_for_msg_start = True 
    while is_waiting_for_msg_start:
        if nic.nic_recv_from_port(port) == "1":
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