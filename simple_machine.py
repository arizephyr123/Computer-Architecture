PRINT_TIM       = 0b00000001
HALT            = 0b00000010
PRINT_NUM       = 0b00000011
# command that will put something into registers
SAVE            = 0b00000100
PRINT_REGISTER  = 0b00000101
ADD             = 0b00000110

memory = [0] * 256



memory = [
    PRINT_TIM,
    PRINT_NUM,
    42,
    SAVE, # SAVE into R2, the number 10
    2, 
    10, 
    SAVE, # SAVE into R2, the number 10
    3, 
    10, 
    ADD,    #registers[2] = registers[2] + registers[3]
    2, 
    3, 
    PRINT_REGISTER,
    HALT
]



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

    elif commamnd == ADD:
        # pull out args
        reg_idx_1 = memory

        # add registers together

        # implement program counter


    elif command == HALT:
        running = False

    else:
        print('unknown command!')
        running = False

    pc += 1