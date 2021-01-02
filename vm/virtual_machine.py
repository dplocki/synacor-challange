from vm.debugger import print_debug
from vm.opt_codes import OptCode


class VirtualMachine():

    def __init__(self, io):
        self.stack = []
        self.registers = {index: 0 for index in range(32768, 32776)}
        self.memory = [0] * (2**16 - 1)
        self.io = io

    def to_number(self, value):
        if is_register(value):
            return self.registers[value]

        if value >= 32776:
            raise Exception(f'Invalid numeric value: {value}')

        return value

    def write(self, where, what):
        what %= 32768

        if 0 <= where <= 32767:
            self.memory[where] = what
        elif 32768 <= where <= 32775:
            self.registers[where] = what
        else:
            raise Exception(f'Unknown address: {where}')

    def read(self, where):
        if 0 <= where <= 32767:
            return self.memory[where]
        elif is_register(where):
            return self.registers[where]

        raise Exception(f'Unknown address: {where}')

    def run(self):
        index = 0
        get_next_value = lambda: (index + 1, self.memory[index])

        while True:
            self.on_new_instruction(index)
            index, opcode = get_next_value()

            if opcode == OptCode.HALT:
                # stop execution and terminate the program
                self.on_program_halt()
                return

            elif opcode == OptCode.SET:
                # set register <a> to the value of <b>
                index, a = get_next_value()
                index, b = get_next_value()

                assert is_register(a)
                self.write(a, self.to_number(b))

            elif opcode == OptCode.PUSH:
                # push <a> onto the stack
                index, a = get_next_value()

                self.stack.append(self.to_number(a))

            elif opcode == OptCode.POP:
                # remove the top element from the stack and write it into <a>; empty stack = error
                index, a = get_next_value()

                self.write(a, self.stack.pop())

            elif opcode == OptCode.EQ:
                # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, 1 if self.to_number(b) == self.to_number(c) else 0)

            elif opcode == OptCode.GT:
                # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, 1 if self.to_number(b) > self.to_number(c) else 0)

            elif opcode == OptCode.JMP:
                # jump to <a>
                index, a = get_next_value()

                index = self.to_number(a)

            elif opcode == OptCode.JT:
                # if <a> is nonzero, jump to <b>
                index, a = get_next_value()
                index, b = get_next_value()

                if self.to_number(a) != 0:
                    index = self.to_number(b)

            elif opcode == OptCode.JF:
                # if <a> is zero, jump to <b>
                index, a = get_next_value()
                index, b = get_next_value()

                if self.to_number(a) == 0:
                    index = self.to_number(b)

            elif opcode == OptCode.ADD:
                # assign into <a> the sum of <b> and <c> (modulo 32768)
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) + self.to_number(c))

            elif opcode == OptCode.MULT:
                # store into <a> the product of <b> and <c> (modulo 32768)
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) * self.to_number(c))

            elif opcode == OptCode.MOD:
                # store into <a> the remainder of <b> divided by <c>
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) % self.to_number(c))

            elif opcode == OptCode.AND:
                # stores into <a> the bitwise and of <b> and <c>
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) & self.to_number(c))

            elif opcode == OptCode.OR:
                # stores into <a> the bitwise or of <b> and <c>
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) | self.to_number(c))

            elif opcode == OptCode.NOT:
                # stores 15-bit bitwise inverse of <b> in <a>
                index, a = get_next_value()
                index, b = get_next_value()

                self.write(a, ~(self.to_number(b)))

            elif opcode == OptCode.RMEM:
                # read memory at address <b> and write it to <a>
                index, a = get_next_value()
                index, b = get_next_value()

                self.write(a, self.read(self.to_number(b)))

            elif opcode == OptCode.WMEM:
                # write the value from <b> into memory at address <a>
                index, a = get_next_value()
                index, b = get_next_value()

                self.write(self.read(a), self.to_number(b))

            elif opcode == OptCode.CALL:
                # write the address of the next instruction to the stack and jump to <a>
                index, a = get_next_value()

                self.stack.append(index)
                index = self.to_number(a)

            elif opcode == OptCode.RET:
                # remove the top element from the stack and jump to it; empty stack = halt
                if not self.stack:
                    self.on_program_halt()
                    return

                index = self.stack.pop()

            elif opcode == OptCode.OUT:
                # write the character represented by ascii code <a> to the terminal
                index, a = get_next_value()

                self.io.write(self.to_number(a))

            elif opcode == OptCode.IN:
                # read a character from the terminal and write its ascii code to <a>;
                # it can be assumed that once input starts, it will continue until a newline is encountered;
                # this means that you can safely read whole lines from the keyboard and trust that they will be fully read
                index, a = get_next_value()

                self.write(a, self.io.read())

            elif opcode == OptCode.NOOP:
                # no operation
                pass

            else:
                raise Exception(f'Unknown opcode {opcode}')

    def load_program(self, program: list):
        for index, instruction in enumerate(program):
            self.memory[index] = instruction

    def on_new_instruction(self, index: int) -> None:
        pass

    def on_program_halt(self) -> None:
        pass


def is_register(number: int) -> bool:
    return 32768 <= number <= 32775
