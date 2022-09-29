import nic_interface as nic

nic.initialize_communication(1)

input_val = input("are you receiving (r) or sending (s) ")
if(input_val == "r"):
    nic.receive_message(1)
elif(input_val == "s"):
    while True:
        input_msg = input("What message would you like to send ")
        nic.send_message(1,input_msg)