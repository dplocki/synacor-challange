from vm.debugger import print_debug


class VirtualMachine():

    def __init__(self):
        self.stack = []
        self.registers = {index: 0 for index in range(32768, 32776)}
        self.memory = [0] * (2**16 - 1)
        self.io = None

    def set_io(self, io):
        self.io = io

    def write(self, where, what):
        what %= 32768

        if 0 <= where <= 32767:
            self.memory[where] = what
        elif 32768 <= where <= 32775:
            self.registers[where] = what
        else:
            raise Exception(f'Unknown address: {where}')

    def to_number(self, value):
        if is_register(value):
            return self.registers[value]

        if value >= 32776:
            raise Exception(f'Invalid numeric value: {value}')

        return value

    def read(self, where):
        if 0 <= where <= 32767:
            return self.memory[where]
        elif is_register(where):
            return self.registers[where]

        raise Exception(f'Unknown address: {where}')

    def load_program(self, program: list):
        for index, instruction in enumerate(program):
            self.memory[index] = instruction

    def run(self):
        index = 0
        def get_next_value(): return (index + 1, self.memory[index])

        while True:
            #print_debug(index, self.memory)
            index, opcode = get_next_value()

            if opcode == 0:  # halt
                # stop execution and terminate the program
                return

            elif opcode == 1:  # set
                # set register <a> to the value of <b>
                index, a = get_next_value()
                index, b = get_next_value()

                assert is_register(a)
                self.write(a, self.number(b))

            elif opcode == 2:  # push:
                # push <a> onto the stack
                index, a = get_next_value()

                self.stack.append(self.to_number(a))

            elif opcode == 3:  # pop
                # remove the top element from the stack and write it into <a>; empty stack = error
                index, a = get_next_value()

                self.write(a, self.stack.pop())

            elif opcode == 4:  # eq
                # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, 1 if self.to_number(b) == self.to_number(c) else 0)

            elif opcode == 5:  # gt
                # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, 1 if self.to_number(b) > self.to_number(c) else 0)

            elif opcode == 6:  # jmp
                # jump to <a>
                index, a = get_next_value()

                index = self.to_number(a)

            elif opcode == 7:  # jt
                # if <a> is nonzero, jump to <b>
                index, a = get_next_value()
                index, b = get_next_value()

                if self.to_number(a) != 0:
                    index = self.to_number(b)

            elif opcode == 8:  # jf
                # if <a> is zero, jump to <b>
                index, a = get_next_value()
                index, b = get_next_value()

                if self.read(a) == 0:
                    index = self.readFromMemory(b)

            elif opcode == 9:  # add
                # assign into <a> the sum of <b> and <c> (modulo 32768)
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) + self.to_number(c))

            elif opcode == 10:  # mult
                # store into <a> the product of <b> and <c> (modulo 32768)
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) * self.to_number(c))

            elif opcode == 11:  # mod
                # store into <a> the remainder of <b> divided by <c>
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) % self.to_number(c))

            elif opcode == 12:  # and
                # stores into <a> the bitwise and of <b> and <c>
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) & self.to_number(c))

            elif opcode == 13:  # or
                # stores into <a> the bitwise or of <b> and <c>
                index, a = get_next_value()
                index, b = get_next_value()
                index, c = get_next_value()

                self.write(a, self.to_number(b) | self.to_number(c))

            elif opcode == 14:  # not
                # stores 15-bit bitwise inverse of <b> in <a>
                index, a = get_next_value()
                index, b = get_next_value()

                self.write(a, ~(self.to_number(b)))

            elif opcode == 15:  # rmem
                # read memory at address <b> and write it to <a>
                index, a = get_next_value()
                index, b = get_next_value()

                self.write(a, self.read(b))

            elif opcode == 16:  # wmem
                # write the value from <b> into memory at address <a>
                index, a = get_next_value()
                index, b = get_next_value()

                self.write(self.read(a), self.to_number(b))

            elif opcode == 17:  # call
                # write the address of the next instruction to the stack and jump to <a>
                index, a = get_next_value()

                self.stack.append(index)
                index = self.to_number(a)

            elif opcode == 18:  # call
                # remove the top element from the stack and jump to it; empty stack = halt
                if not self.stack:
                    return

                index = self.stack.pop()

            elif opcode == 19:  # out a
                # write the character represented by ascii code <a> to the terminal
                index, a = get_next_value()

                self.io.write(self.read(a))

            elif opcode == 20:  # in
                # read a character from the terminal and write its ascii code to <a>;
                # it can be assumed that once input starts, it will continue until a newline is encountered;
                # this means that you can safely read whole lines from the keyboard and trust that they will be fully read
                index, a = get_next_value()

                self.writeInMemory(a, self.io.read())

            elif opcode == 21:  # noop
                # no operation
                pass

            else:
                raise Exception(f'Unknown opcode {opcode}')


def is_register(number: int) -> bool:
    return 32768 <= number <= 32775
