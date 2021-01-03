import sys
import ast

from vm.utils import load_program
from vm.virtual_machine import VirtualMachine
from vm.standard_io import StandardIO
from vm.debug_virtual_machine import DebugVirtualMachine

DEBUG_FLAG = '-d'
LOAD_DUMP_FLAG = '-l'


args = sys.argv[1:] if len(sys.argv) > 1 else []
vm = DebugVirtualMachine() if DEBUG_FLAG in args else VirtualMachine(StandardIO())

if LOAD_DUMP_FLAG in args:
    dump_file_name = args[args.index(LOAD_DUMP_FLAG) + 1]
    with open(dump_file_name, 'rt') as dump_file:
        dump = ast.literal_eval(dump_file.read())

        vm.registers = dump['registers']
        vm.stack = dump['stack']
        vm.load_memory(dump['memory'])
        vm.run(index=dump['index'])
else:
    vm.load_memory(load_program('challenge.bin'))
    vm.run()
