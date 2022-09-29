import pigpio
import time

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

class Packet:
  def __init__(self, bit_msg):
    self.bit_msg = bit_msg
    getbinary = lambda x, n: format(x, "b").zfill(n)
    self.header = getbinary(len(self.bit_msg), 3)
    self.header = "1"+ self.header
    self.bit_msg = self.bit_msg + "0" # Need to end with 0 so that the bit stream returns to 0
    self.total_msg = self.header + self.bit_msg

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
def nic_recv() -> str:
    reciever_4bit_representation = [0,0,0,0]
    reciever_4bit_representation[0] = str(pi.read(26))
    reciever_4bit_representation[1] = str(pi.read(24))
    reciever_4bit_representation[2] = str(pi.read(22))
    reciever_4bit_representation[3] = str(pi.read(20))
    return "".join(reciever_4bit_representation) 

# ================== send receive functions ===================

def initialize_communication(port):
    print(f"initializing communication, sending on port {port}")
    nic_port_send("1", port)
    read_value = nic_recv() 
    print("reading nic port values, wating for verification")
    while (read_value[int(port) - 1] != "1"):
        read_value = nic_recv() 
        print("reading nic port values, wating for verification")
    print("verification received")
    time.sleep(1)
    nic_port_send("0",port)
    return True

# send
def send_message(port: str, message: str):
    new_packet = Packet(message)
    for bit in new_packet.total_msg:
        nic_port_send(bit, port)
        time.sleep(0.1)

# receive 
def receive_message(port):
    msg = ""
    msg_size = ""# Binary rep of msg size
    is_decoding_header = False
    is_decoding_msg = False
    while True:
        if(is_decoding_header):
            time.sleep(0.1)
        received_msg = nic_recv()[port - 1]
        # check for start of msg
        if(received_msg == "1" and not is_decoding_msg and not is_decoding_header):
            # print("Now decoding header")
            # print(received_msg)
            is_decoding_header = True
            continue

        # decoding header
        if(is_decoding_header and len(msg_size) < 3):
            msg_size += received_msg
            # print("adding to msg_size header")
        
        # add to the msg if the msg hasn't reached its max length
        if(msg_size == 3 and len(msg) != int(msg_size,2)):
            # Now we decode msg
            is_decoding_msg = True
            msg += received_msg
        elif(msg_size != "" and len(msg) == int(msg_size,2)): # print when msg is done
            print(msg)
            break

# zeros out the ports
def flush():
    nic_send("0000")

