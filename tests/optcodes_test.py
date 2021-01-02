import unittest
from vm.virtual_machine import VirtualMachine


class TestOptCodes(unittest.TestCase):

    def test_bitwise(self):
        provided = int('000000000000011', 2)
        expected = int('111111111111100', 2)

        result = execute_bitwise(provided)

        self.assertEqual(result, expected, f'Expected {expected}, but result is {result}')


def execute_bitwise(paramater):
    vm = VirtualMachine()
    vm.load_program([14, 32769, paramater])
    vm.run()
    return vm.registers[32769]
