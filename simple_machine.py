PRINT_TIM   = 0b00000001
HALT        = 0b00000010
PRINT_NUM   = 0b00000011

memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    HALT
]

# cpu should now step through memory and take the actions based on commands it finds

# a data-driven machine

# program counter
pc = 0
running = True

while running:
    command = memory[pc]
    pc +=1

    if command == PRINT_TIM:
        print('tim!')

    elif command == HALT:
        running = False