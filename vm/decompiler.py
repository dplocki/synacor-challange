from vm.debug_virtual_machine import OPTCODES_WITH_PARAMETERS, parameter_to_string


def generate_listing(program: [int]) -> None:

    def out_param(value: int) -> str:
        if value == 10:
            return '\\n'
        elif value <= 255:
            return chr(value)

        return parameter_to_string(value)


    index, index_max = 0, len(program)

    while index < index_max:
        print(f'{index:>7}: ', end='')

        if program[index] in OPTCODES_WITH_PARAMETERS:
            name, parameters_number = OPTCODES_WITH_PARAMETERS[program[index]]

            print(f'{name:>7}', f'{" ".join(map(parameter_to_string, program[index + 1: index + 1 + parameters_number])):40}', end='')

            if name == 'out':
                print('|', out_param(program[index + 1]), end='')

            print()
            index += parameters_number
        else:
            print(index)

        index += 1
