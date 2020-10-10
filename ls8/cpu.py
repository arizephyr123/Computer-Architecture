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
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# ALU methods
ADD = 0b10100000    
SUB = 0b10100001 
MUL = 0b10100010    # 162
DIV = 0b10100011
MOD = 0b10100100
CMP = 0b10100111  
AND = 0b01101001
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100

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
            SUB: self.sub, 
            MUL: self.mul,
            DIV: self.div,
            MOD: self.mod,
            CMP: self.comp,  
            AND: self.bw_and,
            OR: self.bw_or,
            XOR: self.bw_xor,
            NOT: self.bw_not,
            SHL: self.shl,
            }

        
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
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
        elif op == "AND":
            self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] << self.reg[reg_b]
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
        self.reg[MAR] = MDR

    def hlt(self):
        """ halt CPU, exit emulator """
        self.running = False
        sys.exit()

    def ldi(self):
        """ load "immediate" - set this register to this value """
        reg_num = self.ram[self.pc+1]
        value = self.ram[self.pc+2]

        self.ram_write(reg_num, value)
        self.pc +=3
        

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
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('MUL', reg_a, reg_b)
        self.pc +=3

    def comp(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('CMP', reg_a, reg_b)
        self.pc +=3

    def bw_and(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('AND', reg_a, reg_b)
        self.pc +=3

    def bw_not(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('NOT', reg_a, reg_b)
        self.pc +=3

    def bw_or(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('OR', reg_a, reg_b)
        self.pc +=3

    def bw_xor(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('XOR', reg_a, reg_b)
        self.pc +=3


    def div(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('DIV', reg_a, reg_b)
        self.pc +=3

    def mod(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('MOD', reg_a, reg_b)
        self.pc +=3

    
    def sub(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('SUB', reg_a, reg_b)
        self.pc +=3

    
    def shl(self):
        reg_a = self.ram[self.pc+1]
        reg_b = self.ram[self.pc+2]
        self.alu('SHL', reg_a, reg_b)
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
        pass

    def pop(self):
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
        pass


    def call(self):
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
        pass


    def ret(self):
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
        pass


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
        """
        if self.flag == 1:
            self.jmp()
        else:
            self.pc +=2
        


    def jne(self):
        """
        If `E` flag is clear (false, 0), jump to the address stored in the given register.
        """
        if self.flag != 1:
            self.jmp()
        else:
            self.pc +=2
    
    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running == True:
            # print('regs =>', self.reg)
            # ir => instruction register
            # in ram at program counter index
            ir = self.ram[self.pc]
            # print(f'run pc -> {self.pc}')
            # print('ir', ir)
            

            if ir in self.ir_methods:
                # grab/ call ir method from ir_methods dictionay
                # print(f'ir_methods[{ir}] -> {self.ir_methods[ir]}')
                self.ir_methods[ir]()

            else:
                print(f'Invalid Instruction {ir} at address {self.pc}')
                self.running == False
                sys.exit()
