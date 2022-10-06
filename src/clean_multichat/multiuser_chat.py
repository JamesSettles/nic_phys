import nic_interface as nic
import network_interface as net
import threading
import sys
# assumes all nics are flushed
BIT_WIDTH = 0.1
nic.flush()
# port connections are put in as command line args
ports = sys.argv[1:]
# check for bad args 
if len(ports) < 1:
    print("ERROR: Must specify multiple ports for args")
    exit(-1)

for i in range(len(ports)):
    if ports[i] == "null":
        ports[i] = None;
    else:
        ports[i] = int(ports[i])

usr_name = input("Enter a single char username ")
if len(usr_name) != 1:
    raise Exception("Usr name not char ")

read_thread = threading.Thread(target=net.receive,args=(BIT_WIDTH,ports[0],ports[1]))
read_thread.start()
while True:
    msg = input(f"{usr_name}: ")
    net.broadcast(msg,usr_name,BIT_WIDTH)
