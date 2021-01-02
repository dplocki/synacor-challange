class MemoryIO():
    def __init__(self):
        self.log = []

    def write(self, what):
        self.log.append(what)
