from vm.utils import load_program
from vm.virtual_machine import VirtualMachine
from vm.standard_io import StandardIO


vm = VirtualMachine()
vm.set_io(StandardIO())
vm.load_program(load_program('challenge.bin'))
vm.run()
