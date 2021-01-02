from vm.virtual_machine import VirtualMachine
from vm.memory_io import MemoryIO
from vm.debugger import print_debug


class DebugVirtualMachine(VirtualMachine):
    
    def __init__(self):
        VirtualMachine.__init__(self, MemoryIO())

    def on_new_instruction(self, index: int) -> None:
        print_debug(index, self.memory)

    def on_program_halt(self) -> None:
        print(''.join(map(chr, self.io.log)))
