from vm.utils import load_program
from vm.virtual_machine import VirtualMachine
from vm.standard_io import StandardIO
from vm.debug_virtual_machine import DebugVirtualMachine


vm = VirtualMachine(StandardIO)
#vm = DebugVirtualMachine()

vm.load_program(load_program('challenge.bin'))
vm.run()
