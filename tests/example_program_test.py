import unittest

from .test_io import TestIO
from vm.virtual_machine import VirtualMachine


class TestExampleProgram(unittest.TestCase):

    def test_run_example_program(self):
        output = TestIO()
        vm = VirtualMachine()
        vm.set_io(output)
        vm.registers[32769] = 100
        vm.load_program([9, 32768, 32769, 4, 19, 32768])
        vm.run()

        self.assertEqual(vm.registers[32768], 104)
        self.assertEqual(output.log, [chr(104)])
