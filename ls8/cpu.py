"""CPU functionality."""

import sys




HLT = 0b00000001  # halt CPU, exit emulator
LDI = 0b10000010  # load "immediate" - set this register to this value
PRN = 0b01000111  # prints numeric value stored in register
# ALU methods
ADD = 0b10100000
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 # program counter
        self.running = False
        self.ir_methods = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            ADD: self.add,
            MUL: self.mul,

        }
        # fl = 
        # ie = 

        pass

    def load(self, file_path):
        """Load a program into memory."""

        address = 0

        with open(file_path) as program:
            for line in program:
                instruction = line.strip().split()
                if len(instruction) == 0 or instruction[0] == '#':
                    continue
                try:
                    # 
                    self.ram[address] = int(instruction[0], 2)
                except ValueError:
                    print('Invalid command: {instruction[0]}')

        address +=1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        print(self.reg[MAR])

    def ram_write(self, MAR, MDR):
        """Write RAM from memory data register to MAR"""
        self.reg[MAR] = MDR

    def hlt(self):
        """ halt CPU, exit emulator """
        self.running = False
        sys.exit()

    def ldi(self):
        """ load "immediate" - set this register to this value """
        pass

    def prn(self):
        """  """
        pass

    def add(self):
        """  """
        pass

    def mul(self):
        """  """
        pass


    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running == True:
            # ir => instruction register
            # in ram at program counter index
            ir = self.ram[self.pc]

            if ir in self.ir_methods:
                self.ir_methods()
