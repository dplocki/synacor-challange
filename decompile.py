from sys import argv
from vm.utils import load_dump_file
from vm.decompiler import generate_listing


LOAD_DUMP_FLAG = '-l'

args = argv[1:] if len(argv) > 1 else []
if LOAD_DUMP_FLAG not in args:
    print('Please provide the dump file to read from')
else:
    dump_file_name = args[args.index(LOAD_DUMP_FLAG) + 1]
    dump = load_dump_file(dump_file_name)

    generate_listing(dump['memory'])
