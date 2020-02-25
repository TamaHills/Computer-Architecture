"""CPU functionality."""
from typing import List
import sys


HLT = 1
LDI = 2
PRN = 7
class MASK:
    OP = 15
    ALU = 32


class CPU:
    """Main CPU class."""
    def __init__(self) -> None:
        """Construct a new CPU."""
        self.alu_table = { 0: 'ADD', 1: 'SUB', 2: 'MUL', 3: 'DIV' }
        self.branch_table = {}
        
        self.branch_table[LDI] = self.LDI
        self.branch_table[PRN] = self.PRN
        self.branch_table[HLT] = self.HLT


        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.IR = 0
        self.FL = 0
        self.MDR = 0
        self.MAR = 0


    def load(self, file) -> None:
        """Load a program into memory."""
        program = open(file, 'r').readlines()

        address = 0

        for line in program:
            # Parse out comments
            comment_split = line.strip().split("#")

            # Cast the numbers from strings to ints
            value = comment_split[0].strip()

            # Ignore blank lines
            if value == "":
                continue

            num = int(value, 2)

            self.ram[address] = num
            address += 1


    def alu(self, op: str, reg_a: int, reg_b: int) -> None:
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self/reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self) -> None:
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
    def ram_read(self, addr: int) -> int:
        if addr > 255:
            print('MEMORY ADDRESS OUT OF BOUNDS')
            exit()

        return self.ram[addr]

    def ram_write(self, addr: int, value: int) -> None:
        if addr > 255:
            print('MEMORY ADDRESS OUT OF BOUNDS')
            exit()

        self.ram[addr] = value

    def PRN(self) -> None:
        op_a = self.ram_read(self.pc + 1)
        if op_a < 8:
            print(self.reg[op_a])
            self.pc += 1
    
    def LDI(self) -> None:
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.reg[op_a] = op_b
        self.pc += 2
    
    def HLT(self) -> None:
        exit()

    def run(self) -> None:
        """Run the CPU."""
        self.pc = 0
        try:
            while True:
                word = self.ram_read(self.pc) 
                op = word & MASK.OP

                op_a = self.ram_read(self.pc + 1)
                op_b = self.ram_read(self.pc + 2)

                # print(f'{op}')
                if (word & MASK.ALU) == MASK.ALU:
                    self.alu(self.alu_table[op], op_a, op_b)
                    self.pc += 2
                elif self.branch_table.get(op):
                    self.branch_table[op]()

                self.pc += 1

        except KeyboardInterrupt:
            self.trace()
