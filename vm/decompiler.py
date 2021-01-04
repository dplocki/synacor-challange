from vm.debug_virtual_machine import OPTCODES_WITH_PARAMETERS


def read_program(program: [int]) -> [tuple]:
    index, index_max = 0, len(program)
    while index < index_max:
        current = program[index]
        if current not in OPTCODES_WITH_PARAMETERS:
            yield index, None, current
        else:
            name, parameters_number = OPTCODES_WITH_PARAMETERS[current]
            yield index, name, tuple(program[index + 1: index + 1 + parameters_number])
            index += parameters_number

        index += 1
