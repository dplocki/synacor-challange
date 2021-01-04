from sys import argv

from vm.utils import load_program, load_dump_file
from vm.virtual_machine import VirtualMachine
from vm.standard_io import StandardIO
from vm.debug_virtual_machine import DebugVirtualMachine

DEBUG_FLAG = '-d'
LOAD_DUMP_FLAG = '-l'


vm = DebugVirtualMachine() if DEBUG_FLAG in argv else VirtualMachine(StandardIO())

if LOAD_DUMP_FLAG in argv:
    dump_file_name = argv[argv.index(LOAD_DUMP_FLAG) + 1]
    dump = load_dump_file(dump_file_name)

    vm.registers = dump['registers']
    vm.stack = dump['stack']
    vm.load_memory(dump['memory'])
    vm.index = dump['index']
else:
    vm.load_memory(load_program('challenge.bin'))

vm.run()
