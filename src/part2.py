import nic_interface as nic
import threading
import time
nic.flush()
nic.initialize_communication(1)

# Have one thread be listening for read msgs
# Another thread to write msgs 

def listen_for_read_msgs():
    while True:
        nic.receive_message(1, .1)
        time.sleep(0.01) # sleep for a bit 

def listen_for_write_msgs():
    while True:
        msg = input("What message would you like to send ")
        nic.send_message(1, msg, .1)


read_thread = threading.Thread(target=listen_for_read_msgs,args=())
write_thread = threading.Thread(target=listen_for_write_msgs,args=())

read_thread.start()
write_thread.start()