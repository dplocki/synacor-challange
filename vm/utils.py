def load_program(file_name: str):
    with open(file_name, mode='rb') as file:
        while True:
            tmp = file.read(2)
            if tmp:
                yield int.from_bytes(tmp, byteorder='little')
            else:
                return
