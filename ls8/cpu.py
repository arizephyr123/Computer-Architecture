"""CPU functionality."""

import sys

HLT = 0b00000001  # 1-> halt CPU, exit emulator
LDI = 0b10000010  # 130-> load "immediate" - set this register to this value
PRN = 0b01000111  # 71-> prints numeric value stored in register
# ALU methods
ADD = 0b10100000    # 
MUL = 0b10100010    # 162

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 # program counter
        self.sp = 7 # stack pointer (last index of registers)
        self.reg[self.sp] = 0xF4 # stack pointer set here why??- start toward end of RAM and move down(decrement index)??
        self.running = False
        self.ir_methods = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            ADD: self.add,
            MUL: self.mul,
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
    
    def run(self):
        """Run the CPU."""
        self.running = True
        # self.trace()
        # print('in run\n', self.ram)

        while self.running == True:
            # print('regs =>', self.reg)
            # ir => instruction register
            # in ram at program counter index
            ir = self.ram[self.pc]
            # print(f'pc -> {self.pc}')
            # print('ir', ir)
            


            if ir in self.ir_methods:
                # grab/ call ir method from ir_methods dictionay
                # print(f'ir_methods[{ir}] -> {self.ir_methods[ir]}')
                self.ir_methods[ir]()

            else:
                print(f'Invalid Instruction {ir} at address {self.pc}')
                self.running == False
                sys.exit()
