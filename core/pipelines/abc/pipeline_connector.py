class Connector:
    def __init__(self):
        self.connections = {}

    def add_connection(self, name, connection):
        self.connections[name] = connection

    def connect(self, name, starter, finisher, last):
        return self.connections[name](starter, finisher, last)
