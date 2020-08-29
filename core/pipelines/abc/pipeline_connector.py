class Connector:
    def __init__(self, starter, finisher):
        self.starter = starter
        self.finisher = finisher
        self.connections = {}

    def add_connection(self, name, connection):
        self.connections[name] = connection

    def connect(self, name):
        self.connections[name](self.starter, self.finisher)
