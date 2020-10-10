PRINT_TIM       = 0b00000001
HALT            = 0b00000010
PRINT_NUM       = 0b00000011
SAVE            = 0b00000100 # LDI, put something into registers
PRINT_REGISTER  = 0b00000101
ADD             = 0b00000110
PUSH            = 0b01000111
POP             = 0b01001000
CALL            = 0b01011001
RET             = 0b00011010

memory = [0] * 256

# memory = [
#     SAVE,
#     0,
#     8, # idx of subroutine below 
#     PRINT_NUM, 
#     99, 
#     CALL, 
#     0, 
#     HALT, 
#     PRINT_TIM,  # address, aka index of subroutine
#     PRINT_TIM, 
#     RET
# ]


# memory = [
#     PRINT_TIM,
#     PRINT_NUM,
#     42,
#     SAVE, # SAVE into R2, the number 10
#     2, 
#     10, 
#     SAVE, # SAVE into R2, the number 10
#     3, 
#     10, 
#     ADD,    #registers[2] = registers[2] + registers[3]
#     2, 
#     3, 
#     PRINT_REGISTER,
#     HALT
# ]



# cabinets in your shop : registers
# storage unit: cache
# warehouse outside town: RAM

#R0-R7
registers = [0] * 8

# cpu should now step through memory and take the actions based on commands it finds

# a data-driven machine

# program counter, a pointer
pc = 0
running = True

while running:
    command = memory[pc]

    if command == PRINT_TIM:
        print('tim!')

    elif command == PRINT_NUM:
        pc +=1
        number = memory[pc]
        print(number)

    elif command == SAVE:
        # get args 
        # pc+1 is reg idx, pc+2 is value to be saved
        reg_idx = memory[pc+1]
        value = memory[pc+2]
        # put the value into the correct register
        registers[reg_idx] = value
        # increment program counter by 2
        ## 2+1 below == 3-byte command
        pc += 2

    elif command == ADD:
        # pull out args
        reg_idx_1 = memory

        # add registers together

        # implement program counter
    elif command == POP:
        # copy value from the address pointed to by the 'SP' to the given register
        # we need SP address
        SP = registers[7]
        # need value fro mthat address
        value = memory[SP]
        # we need the register address
        reg_idx = memory[pc+1]
        registers[reg_idx] = value
        # increment SP where stored in registers
        registers[7] += 1

    elif command == CALL:
        # push command address after CALL onto stack
        ## PC points to CALL address right now
        ## get command address
        ret_address = pc+2

        ## then push the return address into the stack
        ### Step 1: decrement the SP, stored in R7
        registers[7] -= 1
        ### Step 2: store the value at the SP address
        SP = registers[7]
        memory[SP] = ret_address

        # set PC to address stored in given register
        ## retrieve address from register
        ### find which register
        reg_idx - pc+1
        ### look in register to find address
        subroutine_address = registers[reg_idx]
        pc = subroutine_address

    elif command == RET:
        # pop value from top of stack and store in pc
        SP = registers[7]
        return_address = memory[SP]

        pc = return_address
        # decrement for push, increment for pop
        registers[7] += 1






    elif command == HALT:
        running = False

    else:
        print('unknown command!')
        running = False

    pc += 1