"""
Helper functions for converting text to binary
"""
# Each char converts to 7 bits
def char_to_bin(char : str):
    if(len(char) != 1):
        raise Exception("ERROR: char must be of length 1")    
    bin_rep = bin(int.from_bytes(char.encode(), 'big'))
    # we want to remove the 0b portion of the bin_rep
    bin_rep = bin_rep[2:]
    return bin_rep
"""
Takes in str representation of a 7 bit binary sequence 
returns a char
"""
def bin_to_char(bin_rep) -> str:
    int_rep = int(bin_rep,2) # converts from binary representation to integer
    try:
        char_rep = int_rep.to_bytes((int_rep.bit_length() + 7) // 8, 'big').decode()
    except UnicodeDecodeError as e:
        print(f"ERROR decoding bin rep: {bin_rep}")
    return char_rep
"""
Takes in a str and converts it to a list of 7 bit binary sequences
"""
def str_to_binary(string) -> list:
    bin_reps = []
    for character in string:
        bin_reps.append(char_to_bin(character))
    return bin_reps

def bin_to_str(bin_reps) -> str:
    str_rep = ""
    for bin_rep in bin_reps:
        str_rep += bin_to_char(bin_rep)
    return str_rep