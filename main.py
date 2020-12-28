class StandardOutput():

    def write(self, what):
        print(what)


class TestOutput():
    def __init__(self):
        self.log = []

    def write(self, what):
        self.log.append(what)


class VirtualMachine():

    def __init__(self):
        self.stack = []
        self.registers = {i: 0 for i in range(32768, 32776)}
        self.memory = {}
        self.output = None

    def set_output(self, output):
        self.output = output

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

        while index < program_lenght:
            opcode = program[index]
            index += 1

            if opcode == 0: # halt
                return

            if opcode == 9: # add
                self.writeInMemory(
                    program[index],
                    self.readFromMemory(program[index + 1]) + self.readFromMemory(program[index + 2]))

                index += 3

            elif opcode == 19: # out a
                self.output.write(self.readFromMemory(program[index]))
                index += 1

            elif opcode == 21: # noop
                pass

            else:
                raise Exception(f'Unknown opcode {opcode}')


example_program = [9, 32768, 32769, 4, 19, 32768]

output = TestOutput()
vm = VirtualMachine()
vm.set_output(output)
vm.execute_program(example_program)

assert vm.registers[32768] == 4
assert len(output.log) == 1
assert output.log[0] == 4

output = TestOutput()
vm = VirtualMachine()
vm.set_output(output)
vm.registers[32769] = 100
vm.execute_program(example_program)
assert vm.registers[32768] == 104
assert len(output.log) == 1
assert output.log[0] == 104
