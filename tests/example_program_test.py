import unittest

from vm.virtual_machine import VirtualMachine
from vm.memory_io import MemoryIO


class TestExampleProgram(unittest.TestCase):

    def test_run_example_program(self):
        output = MemoryIO()
        vm = VirtualMachine(output)
        vm.registers[32769] = 100
        vm.load_memory([9, 32768, 32769, 4, 19, 32768])
        vm.run()

        self.assertEqual(vm.registers[32768], 104)
        self.assertEqual(output.log, [104])
