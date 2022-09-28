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
  def __init__(bit_msg):
    self.bit_msg = bit_msg
    getbinary = lambda x, n: format(x, "b").zfill(n)
    self.header = getbinary(len(self.bit_msg),3)
    self.header = "1"+ self.header
    self.bit_msg = self.bit_msg + "0" # Need to end with 0 so that the bit stream returns to 0

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
    return True

# send
def send_message(port, message):
    new_packet = Packet(message)
    for bit in new_packet:
        nic_port_send(new_packet, port)

# receive 
def receive_message(port):
    msg = ""
    msg_size = "" # Binary rep of msg size
    is_decoding_header = False
    is_decoding_msg = False
    while True:
        received_msg = nic_recv()[port -1]
        
        if(is_decoding_header and len(msg_size) < 3):
            msg_size += received_msg
        
        if(msg_size == 3 and ):
            # Now we decode msg
            msg += received_msg


        if(received_msg[port - 1] == "1"):
                is_decoding_header = True
        

        



# Set all ports to 0 then 1 then 0 to "clean them"
nic_send("0000")
nic_send("1111")
nic_send("0000")
