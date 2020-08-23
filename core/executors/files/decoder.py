
class Decoder:
    def __init__(self, encoding):
        self.encoding = encoding

    def decode(self, data):
        return data.decode(encoding=self.encoding)