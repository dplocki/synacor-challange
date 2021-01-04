from sys import argv
from vm.utils import load_dump_file
from vm.decompiler import read_program
from vm.debug_virtual_machine import parameter_to_string, format_parameter



def out_param(value: int) -> str:
    if value == 10:
        return '\\n'
    elif value <= 255:
        return chr(value)

    return parameter_to_string(value)


LOAD_DUMP_FLAG = '-l'

args = argv[1:] if len(argv) > 1 else []
if LOAD_DUMP_FLAG not in args:
    print('Please provide the dump file to read from')
else:
    dump_file_name = args[args.index(LOAD_DUMP_FLAG) + 1]
    dump = load_dump_file(dump_file_name)

    decompiled_program = list(read_program(dump['memory']))
    call_indexes = set(paramaters[0] for _, name, paramaters in decompiled_program if name == 'call')

    for index, name, paramaters in decompiled_program:
        print('*' if index in call_indexes else ' ', end='')
        print(f'{index:>7}: ', end='')
        if name:
            print(f'{name:>7}  ', end='')
            if name == 'out':
                print(out_param(paramaters[0]), end='')
            elif name == 'ret':
                print()
            elif paramaters:
                print(*map(format_parameter, map(parameter_to_string, paramaters)), end='')
        else:
            print(paramaters, end='')
        print()
