from core.data.enums import Files


class Reader:

    @staticmethod
    def read(filename, **kwargs):
        print("[Reading from ", filename, "]")
        with open(filename, **kwargs) as f:
            result = f.read()
        return result

    @staticmethod
    def read_raw(filename, enc):
        print("[Reading from ", filename, "]")
        with open(filename, mode="r", encoding=enc, newline='') as f:
            result = f.read()
        return result

    @staticmethod
    def read_byte(filename):
        print("[Reading bytes from ", filename, "]")
        with open(filename, mode="rb") as f:
            result = f.read()
        return result
