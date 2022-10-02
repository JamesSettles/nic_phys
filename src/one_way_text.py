import nic_interface as nic
import time
import text_to_binary as t2bin

nic.flush()
nic.initialize_communication(1)

input_val = input("are you receiving (r) or sending (s) ")
if (input_val == "r"):
    msg_to_print = ""
    while True:
        received_msg = nic.receive_message(1, .1)
        time.sleep(0.01) # sleep for a bit so we dont start reading a msg that isnt there
        if(received_msg != None):
            msg_to_print += received_msg
        else:
            print(msg_to_print)
            msg_to_print = ""
        
elif (input_val == "s"):
    while True:
        msg = input("What message would you like to send ")
        bin_reps = t2bin.str_to_binary(msg)
        bin_reps.append(None)
        for bin_rep in bin_reps:
            nic.send_message(1, bin_rep, .1)