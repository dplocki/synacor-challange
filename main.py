from vm.utils import load_program
from vm.virtual_machine import VirtualMachine
from vm.standard_io import StandardIO


program = list(load_program('challenge.bin'))
vm = VirtualMachine()
vm.set_io(StandardIO())
vm.execute_program(program)
