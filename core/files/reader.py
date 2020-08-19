class Reader:
    DEFAULT_ENCODING = "utf-8-sig"
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def read(self, filename):
        print("[Reading from ", filename, "]")
        with open(filename, **self.kwargs) as f:
            result = f.read()
        return result

    @staticmethod
    def read_text(filename):
        print("[Reading from ", filename, "]")
        with open(filename, mode="r", encoding=Reader.DEFAULT_ENCODING) as f:
            result = f.read()
        return result
    
    @staticmethod
    def read_binary(filename):
        print("[Reading from ", filename, "]")
        with open(filename, mode="rb") as f:
            result = f.read()
        return result
        