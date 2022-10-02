import nic_interface as nic
import threading
import time
import text_to_binary as t2bin

nic.flush()
nic.initialize_communication(1)
# Have one thread be listening for read msgs
# Another thread to write msgs 
BIT_WIDTH = 0.1
def listen_for_read_msgs():
    msg_to_print = ""
    while True:
        received_msg = nic.receive_message(1, BIT_WIDTH)
        time.sleep(0.01) # sleep for a bit so we dont start reading a msg that isnt there
        if(received_msg != None):
            msg_to_print += received_msg
        else:
            print("\n" + msg_to_print)
            msg_to_print = ""
        
def listen_for_write_msgs():
    while True:
        msg = input("What message would you like to send \n")
        bin_reps = t2bin.str_to_binary(msg)
        bin_reps.append(None)
        for bin_rep in bin_reps:
            nic.send_message(1, bin_rep, BIT_WIDTH)


read_thread = threading.Thread(target=listen_for_read_msgs,args=())
write_thread = threading.Thread(target=listen_for_write_msgs,args=())

read_thread.start()
write_thread.start()