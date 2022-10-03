import text_communication as tc
import time

tc.initialize_communication(1)

input_val = input("are you receiving (r) or sending (s) ")
if (input_val == "r"):
    while True:
        tc.receive_message(1, .1)
        time.sleep(0.01) # sleep for a bit so we dont start reading a msg that isnt there

elif (input_val == "s"):
    while True:
        msg = input("What message would you like to send ")
        tc.send_message(1, msg, .1)
