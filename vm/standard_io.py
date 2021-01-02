class StandardIO():

    def write(self, what):
        print(chr(what), end='')

    def read(self):
        return input()
