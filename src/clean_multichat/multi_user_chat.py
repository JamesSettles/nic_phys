import multi_user_chat_helpers as helpers
import physical_layer as nic
import link_layer as link
import threading

# Reads from two ports and sends on same two ports
BIT_WIDTH = 0.1
nic.flush()

port1, port2 = helpers.read_port_args()

usr_name = input("Enter a single char username ")
if len(usr_name) != 1:
    raise Exception("Usr name not char ")
# Two threads for reading
read_thread_1 = threading.Thread(target=helpers.continously_read_msgs,args=(port1,BIT_WIDTH))
read_thread_1.start()
if port2:
    read_thread_2  = threading.Thread(target=helpers.continously_read_msgs,args=(port2,BIT_WIDTH))
    read_thread_2.start()
# Continously prompt user to send msgs
while True:
    if port2:
        msg_to_send = input(f"{usr_name}: ")
        helpers.send_msg_out_on_two_ports(port1,port2,msg_to_send,BIT_WIDTH) # Uses one thread to send
    else:
        msg_to_send = input(f"{usr_name}: ")
        helpers.send_msg_out_on_port(port1,msg_to_send,BIT_WIDTH)
        
