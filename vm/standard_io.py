class StandardIO():

    def __init__(self):
        self.buffor = None

    def write(self, what):
        print(chr(what), end='')

    def read(self):
        if not self.buffor:
            self.buffor = list(input())
            self.buffor.append('\n')
            self.buffor.reverse()

        return ord(self.buffor.pop())
