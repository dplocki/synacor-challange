import sys

from vm.utils import load_program
from vm.virtual_machine import VirtualMachine
from vm.standard_io import StandardIO
from vm.debug_virtual_machine import DebugVirtualMachine


vm = DebugVirtualMachine() if len(sys.argv) > 1 and sys.argv[1] == '-d' else VirtualMachine(StandardIO())
vm.load_memory(load_program('challenge.bin'))
vm.run()
