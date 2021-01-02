import unittest
from vm.virtual_machine import VirtualMachine
from vm.opt_codes import OptCode
from .test_io import TestIO


class TestOptCodes(unittest.TestCase):

    def setUp(self):
        self.vm = VirtualMachine()
        self.io = TestIO()
        self.vm.set_io(self.io)

    def test_bitwise(self):
        provided = int('000000000000011', 2)
        expected = int('111111111111100', 2)

        self.vm.load_program([
            OptCode.NOT, 32769, provided
        ])

        self.vm.run()
        result = self.vm.registers[32769]

        self.assertEqual(result, expected, f'Expected {expected}, but result is {result}')

    def test_out(self):
        self.vm.load_program([
            OptCode.OUT, ord('A')
        ])

        self.vm.run()
        result = self.io.log

        self.assertEqual(result, [65], f'Excepted letter but result is: {result}')
