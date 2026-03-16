import sys

# System Variables
BUFFER_SIZE = 8
VAR_SIZE = 8
RBP_SIZE = 8
ADDR_SIZE = 8

# Null Bytes
buffer = ['\x00'] * BUFFER_SIZE  # simulate uninitialized memory
# adjacent memory layout (simulated stack frame above buffer)
next_var  = list("auth\x00\x00\x00\x00")   # some other variable on the stack
saved_rbp  = list("\xff\xcc\xa8\x10\x00\x00\x00\x00")  # saved base pointer
ret_addr   = list("\x34\x12\x40\x00\x00\x00\x00\x00") # return address: critical target

def write_buffer(user_input):
    """
        Write into the buffer variable, unsafe:
        Grows upwards towards the other segments in the stack.

        Provides Terminal Outputs of Overwritten Segments & Important Information
    """
    # snapshot before writing
    prev_next_var = next_var[:]
    prev_saved_rbp = saved_rbp[:]
    prev_ret_addr = ret_addr[:]

    # Info for Terminal:
    print(f"Input Length: {len(user_input)}")
    print(f"Buffer Size: {BUFFER_SIZE}")
    print(f"Buffer Content: {"".join(buffer)} will now become: {user_input[0:BUFFER_SIZE]} \n")

    if(len(user_input) > BUFFER_SIZE):
        print(f"[OVERFLOW]: Buffer Size of {BUFFER_SIZE} exceeded")
        print(f"Overflow bytes: [{user_input[BUFFER_SIZE:-1]}] will spill into adjacent memory")

    # When an overflow occurs, they should overwrite the these variables in order: next_var, saved_rbp and return_addr
    for i, char in enumerate(user_input):
        if i < BUFFER_SIZE:
            buffer[i] = char

        elif i < VAR_SIZE + 8: # offset
            next_var[i-8] = char

        elif i < RBP_SIZE + 16: # offset
            saved_rbp[i-16] = char

        elif i < ADDR_SIZE + 24:  # offset
            ret_addr[i - 24] = char

    # post-write analysis
    if next_var != prev_next_var:
        print(f"[WARNING] next_var  corrupted: {''.join(prev_next_var)} -> {''.join(next_var)}")
    if saved_rbp != prev_saved_rbp:
        print(f"[WARNING] saved_rbp corrupted: {''.join(prev_saved_rbp)} -> {''.join(saved_rbp)}")
    if ret_addr != prev_ret_addr:
        print(f"[WARNING] ret_addr  HIJACKED:  {''.join(prev_ret_addr)} -> {''.join(ret_addr)}")
        print(f"[CRITICAL] execution would redirect to {''.join(ret_addr)}")

# Print out all Memory Segments
def memory_segment_status():
    print("\n----------Buffer----------")
    print(buffer)
    print("----------Next_Var----------")
    print(next_var)
    print("----------Saved_RBP----------")
    print(saved_rbp)
    print("----------Ret_Addr----------")
    print(ret_addr)

def main():
    print("Buffer Overflow Simulation")

    user_input = input("Input String to Write to Buffer: ",)

    write_buffer(user_input)

    # memory_segment_status()

    # args = sys.argv[1:]
    # if args:
    #     print("Arguments:", args)
    # else:
    #     print("No arguments provided")

    print("Program finished")

if __name__ == "__main__":
    main()