"""CPU functionality."""

import sys
# branch/dispatch table
HLT = 0b00000001  # 1-> halt CPU, exit emulator
LDI = 0b10000010  # 130-> load "immediate" - set this register to this value
PRN = 0b01000111  # 71-> prints numeric value stored in register
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# ALU methods
ADD = 0b10100000    # 
MUL = 0b10100010    # 162

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.flag = [0] * 8
        self.pc = 0 # program counter
        self.sp = 7 # stack pointer (last index of registers)
        self.reg[self.sp] = 0xF4 # F3  Start of Stack, decrements as pushed, grows down
        self.running = False
        self.ir_methods = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne,
            ADD: self.add,
            MUL: self.mul,
            CMP: self.comp,
            }

    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]

    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

    #     # print('ram', self.ram)

        
    def load(self, file_path):
        """Load a program into memory."""

        address = 0

        with open(file_path) as program:
            for line in program:
                instruction = line.strip().split()
                if len(instruction) == 0 or instruction[0] == '#':
                    continue
                try:
                    # save valid instructions into ram
                    self.ram[address] = int(instruction[0], 2)
                except ValueError:
                    print('Invalid command: {instruction[0]}')

                address +=1
    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print('in ALU')
        if op == "ADD":
            # print('in alu ADD')
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            # print('in alu MUL', reg_a, " * ", reg_b)
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                # * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
                print(f'self.reg[{reg_a}]: {self.reg[reg_a]} == self.reg[{reg_b}]: {self.reg[reg_b]}')
                self.flag[7] = 1 # E flag
                print(self.flag)
            elif self.reg[reg_a] < self.reg[reg_b]:
                # * If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
                print(f'self.reg[{reg_a}]: {self.reg[reg_a]} < self.reg[{reg_b}]: {self.reg[reg_b]}')
                self.flag[5] = 1 # L flag
                print(self.flag)
            elif self.reg[reg_a] > self.reg[reg_b]:
                # * If registerA is greater than registerB, set the Greater-than `G` flag to 1, otherwise set it to 0.
                print(f'self.reg[{reg_a}]: {self.reg[reg_a]} > self.reg[{reg_b}]: {self.reg[reg_b]}')
                self.flag[6] = 1 # G flag
                print(self.flag)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def ram_read(self, MAR):
        """Read RAM from memory address register(MAR)."""
        print(self.reg[MAR]) # <-- don't comment out
        self.reg[MAR]

    def ram_write(self, MAR, MDR):
        """Write RAM from memory data register to MAR"""
        # print('in ran_write ==>\n MAR', MAR, '\nMDR', MDR)
        self.reg[MAR] = MDR

    def hlt(self):
        """ halt CPU, exit emulator """
        self.running = False
        sys.exit()

    def ldi(self):
        """ load "immediate" - set this register to this value """
        reg_num = self.ram[self.pc+1]
        value = self.ram[self.pc+2]
        # print('LDI ==> reg#: ', reg_num, 'val: ', value)
        # print('\npc before ->', self.pc)

        self.ram_write(reg_num, value)
        self.pc +=3
        # print('pc after->', self.pc, '\n')
        

    def prn(self):
        """ prints numeric value stored in register by calling ram_read() on reg address """
        reg_num = self.ram[self.pc+1]
        self.ram_read(reg_num)
        self.pc +=2
    
    def add(self):
        """   """
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('ADD', reg_a, reg_b)
        self.pc +=3

    def mul(self):
        """   """
        # print('in mul')
        # print('pc before ->', self.pc)
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        # print(reg_a, reg_b)
        self.alu('MUL', reg_a, reg_b)
        self.pc +=3
        # print('pc after ->', self.pc)

    def comp(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('CMP', reg_a, reg_b)
        self.pc +=3


    def push(self):
        """
        Push the value in the given register on the stack.

        1. Decrement the `SP`.
        2. Copy the value in the given register to the address pointed to by
        `SP`.

        Machine code:
        ```
        01000101 00000rrr
        45 0r
        ```
        """
        # reg_a = self.ram[self.pc+1]
        # reg_b = self.ram[self.pc+2]
        # self.alu('CMP', reg_a, reg_b)
        # self.pc +=3
        pass

    def pop(self):
        pass
        """
        Pop the value at the top of the stack into the given register.

        1. Copy the value from the address pointed to by `SP` to the given register.
        2. Increment `SP`.

        Machine code:
        ```
        01000110 00000rrr
        46 0r
        ```
        """
        # reg_a = self.ram[self.pc+1]
        # reg_b = self.ram[self.pc+2]
        # self.alu('CMP', reg_a, reg_b)
        # self.pc +=3


    def call(self):
        pass
        """
        Calls a subroutine (function) at the address stored in the register.

        1. The address of the ***instruction*** _directly after_ `CALL` is
        pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.

        Machine code:
        ```
        01010000 00000rrr
        50 0r
        ```
        """
        # reg_a = self.ram[self.pc+1]
        # reg_b = self.ram[self.pc+2]
        # self.alu('CMP', reg_a, reg_b)
        # self.pc +=3


    def ret(self):
        pass
        """
        `RET`

        Return from subroutine.

        Pop the value from the top of the stack and store it in the `PC`.

        Machine Code:
        ```
        00010001
        11
        ```
        """
        # reg_a = self.ram[self.pc+1]
        # reg_b = self.ram[self.pc+2]
        # self.alu('CMP', reg_a, reg_b)
        # self.pc +=3


    def jmp(self):
        """
        Jump to the address stored in the given register.
        """
        # get reg num holding address
        reg_num = self.ram[self.pc+1]
        # get address from that reg
        jump_to_address = self.reg[reg_num]
        # update pc to that address
        self.pc = jump_to_address


    def jeq(self):
        """
        If `equal` flag is set (true), jump to the address stored in the given register.

        Machine code:
        ```
        01010101 00000rrr
        55 0r
        ```
        """
        if self.flag == 1:
            self.jmp()
        self.pc +=2
        


    def jne(self):
        """
        If `E` flag is clear (false, 0), jump to the address stored in the given
        register.
        """
        if self.flag == 0:
            self.jmp()
        self.pc +=2


    
    def run(self):
        """Run the CPU."""
        self.running = True
        # self.trace()
        # print('in run\n', self.ram)

        while self.running == True:
            print('regs =>', self.reg)
            # ir => instruction register
            # in ram at program counter index
            ir = self.ram[self.pc]
            print(f'pc -> {self.pc}')
            # print('ir', ir)
            


            if ir in self.ir_methods:
                # grab/ call ir method from ir_methods dictionay
                # print(f'ir_methods[{ir}] -> {self.ir_methods[ir]}')
                self.ir_methods[ir]()

            else:
                print(f'Invalid Instruction {ir} at address {self.pc}')
                self.running == False
                sys.exit()
