import nic_interface as nic
import time
nic.flush()
nic.initialize_communication(1)

input_val = input("are you receiving (r) or sending (s) ")
if (input_val == "r"):
    while True:
        nic.receive_message(1, .1)
        time.sleep(0.01) # sleep for a bit so we dont start reading a msg that isnt there

elif (input_val == "s"):
    while True:
        msg = input("What message would you like to send ")
        nic.send_message(1, msg, .1)
