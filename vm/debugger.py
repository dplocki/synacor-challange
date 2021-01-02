OPTCODES_WITH_PARAMETERS = {
    0: ('halt', 0),
    1: ('set', 2),
    2: ('push', 1),
    3: ('pop', 1),
    4: ('eq', 3),
    5: ('gt', 3),
    6: ('jmp', 1),
    7: ('jt', 2),
    8: ('jf', 2),
    9: ('add', 3),
    10: ('mult', 3),
    11: ('mod', 3),
    12: ('and', 3),
    13: ('or', 3),
    14: ('not', 2),
    15: ('rmem', 2),
    16: ('wmem', 2),
    17: ('call', 1),
    18: ('ret', 0),
    19: ('out', 1),
    20: ('in', 1),
    21: ('noop', 0)
}


def read_param(number: int) -> str:
    if number >= 32768:
        return 'register_' + str(number - 32768)
    else:
        return str(number)


def format_parameter(number: int):
    return f'{number:<12}'


def print_debug(index: int, program: dict):
    name, parameteres = OPTCODES_WITH_PARAMETERS[program[index]]
    print(
        f'{index:<10} ',
        f'{name:>7} ',
        '  '.join(map(format_parameter, map(read_param, program[index + 1:index + 1 + parameteres]))))
