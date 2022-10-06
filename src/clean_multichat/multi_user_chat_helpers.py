import link_layer as link
import text_to_binary as t2bin
import threading
import time
import sys
"""
Read port args in from command line
"""
def read_port_args():
    ports = sys.argv[1:]
    # check for bad args 
    if len(ports) < 1:
        print("ERROR: Must specify multiple ports for args")
        exit(-1)
    for index in range(len(ports)):
        ports[index] = None if ports[index] == "null" else int(ports[index])
    # only reading/writing to two ports 
    return ports[0],ports[1]
"""
Continously read bit msgs, converting them to chars and printing out complete strings
"""
def continously_read_msgs(port,bit_width):
    msg_to_print = ""
    while True:
        bit_msg = link.receive_bit_message(port,bit_width)
        if bit_msg == -1:
            continue
        if (bit_msg != None):
            msg_to_print += t2bin.bin_to_char(bit_msg)
        else:
            print("\n" + msg_to_print)
            msg_to_print = ""
        # sleep for a bit so we dont start reading a msg that isnt there
        time.sleep(bit_width * 0.5) 

def send_msg_out_on_port(port:int,msg:str,bit_width:int):
    bin_reps_of_msg = t2bin.str_to_binary(msg)
    for bin_rep in bin_reps_of_msg:
        link.send_bit_pattern(port,bin_rep,bit_width)
        # sleep a bit between each bit pattern 
        time.sleep(bit_width*0.5)

def send_msg_out_on_two_ports(port1,port2,msg,bit_width):
    write_thread = threading.Thread(target=send_msg_out_on_port, args=(port1,msg,bit_width))
    write_thread.start()
    send_msg_out_on_port(port1,msg,bit_width)


