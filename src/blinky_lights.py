import nic_interface
# CLI for nic_interface lib
while(1==1):
    val = input("""Would you like to send (s) or receive (r)?\n 
                If sending please provide a 4 bit pattern:""")
    if "s " in val or "send " in val:
        split_val = val.split(" ")
        nic_interface.nic_send(split_val[-1])
    elif val == "r" or val == "receive":
       print(nic_interface.nic_recv_all_ports())      