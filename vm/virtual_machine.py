class VirtualMachine():

    def __init__(self):
        self.stack = []
        self.registers = {i: 0 for i in range(32768, 32776)}
        self.memory = {}
        self.io = None

    def set_io(self, io):
        self.io = io

    def writeInMemory(self, where, what):
        what %= 32768

        if 0 <= where <= 32767:
            self.memory[where] = what
        elif 32768 <= where <= 32775:
            self.registers[where] = what
        else:
            raise Exception(f'Unknown address: {where}')

    def readFromMemory(self, where):
        if 0 <= where <= 32767:
            return where
        elif 32768 <= where <= 32775:
            return self.registers[where]
        else:
            raise Exception(f'Unknown address: {where}')

    def execute_program(self, program: list):
        index = 0
        program_lenght = len(program)
        def get_current_program_value(): return (index + 1, program[index])

        while index < program_lenght:
            index, opcode = get_current_program_value()

            if opcode == 0:  # halt
                return

            elif opcode == 1:  # set
                index, a = get_current_program_value()
                index, b = get_current_program_value()

                self.writeInMemory(a, b)

            elif opcode == 2:  # push:
                index, a = get_current_program_value()

                self.stack.append(self.readFromMemory(a))

            elif opcode == 3:  # pop
                index, a = get_current_program_value()
                self.writeInMemory(a, self.stack.pop())

            elif opcode == 4:  # eq
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, 1 if self.readFromMemory(
                    b) == self.readFromMemory(c) else 0)

            elif opcode == 5:  # gt
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, 1 if self.readFromMemory(
                    b) > self.readFromMemory(c) else 0)

            elif opcode == 6:  # jmp
                index, a = get_current_program_value()
                index = self.readFromMemory(a)

            elif opcode == 7:  # jt
                index, a = get_current_program_value()
                index, b = get_current_program_value()

                if self.readFromMemory(a) != 0:
                    index = self.readFromMemory(b)

            elif opcode == 8:  # jf
                index, a = get_current_program_value()
                index, b = get_current_program_value()

                if self.readFromMemory(a) == 0:
                    index = self.readFromMemory(b)

            elif opcode == 9:  # add
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(
                    b) + self.readFromMemory(c))

            elif opcode == 10:  # mult
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(b)
                                   * self.readFromMemory(c))

            elif opcode == 11:  # mod
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(b) %
                                   self.readFromMemory(c))

            elif opcode == 12:  # and
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(b)
                                   & self.readFromMemory(c))

            elif opcode == 13:  # or
                index, a = get_current_program_value()
                index, b = get_current_program_value()
                index, c = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(b)
                                   | self.readFromMemory(c))

            elif opcode == 14:  # not
                index, a = get_current_program_value()
                index, b = get_current_program_value()

                self.writeInMemory(a, ~(self.readFromMemory(b)))

            elif opcode == 15:  # rmem
                index, a = get_current_program_value()
                index, b = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(b))

            elif opcode == 16:  # wmem
                index, a = get_current_program_value()
                index, b = get_current_program_value()

                self.writeInMemory(a, self.readFromMemory(b))

            elif opcode == 17:  # call
                index, a = get_current_program_value()
                self.stack.append(index)
                index = self.readFromMemory(a)

            elif opcode == 18:  # call
                if not self.stack:
                    return

                index = self.stack.pop()

            elif opcode == 19:  # out a
                index, a = get_current_program_value()
                self.io.write(chr(self.readFromMemory(a)))

            elif opcode == 20:  # in
                index, a = get_current_program_value()
                self.writeInMemory(a, self.io.read())

            elif opcode == 21:  # noop
                pass

            else:
                raise Exception(f'Unknown opcode {opcode}')
