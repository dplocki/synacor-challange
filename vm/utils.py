from ast import literal_eval


def load_program(file_name: str):
    with open(file_name, mode='rb') as file:
        while True:
            tmp = file.read(2)
            if tmp:
                yield int.from_bytes(tmp, byteorder='little')
            else:
                return


def load_dump_file(dump_file_name: str) -> dict:
    with open(dump_file_name, 'rt') as dump_file:
        return literal_eval(dump_file.read())
