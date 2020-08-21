from collections.abc import Iterable

class Writer:
    DEFAULT_ENCODING = "utf-8-sig"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def write(self, filename, content):
        print("[Wrtiting to ", filename, "]")
        with open(filename, **self.kwargs) as f:
            f.write(content)
        return content

    def write(filename, content):
        if isinstance(content, str):
            return Writer.write_text(filename, content)
        elif isinstance(content, Iterable):
            return Writer.write_iter(filename, content)
        else:
            return Writer.write_bin(filename, content)

    @staticmethod
    def write_text(filename, content):
        print("[Wrtiting to ", filename, "]")
        with open(filename, mode="w", encoding=Writer.DEFAULT_ENCODING) as f:
            f.write(content)
        return content
    
    @staticmethod
    def write_bin(filename, content):
        print("[Wrtiting to ", filename, "]")
        with open(filename, mode="wb") as f:
            f.write(content)
        return content
        
    @staticmethod
    def write_iter(filename, array):
        print("[Wrtiting to ", filename, "]")
        with open(filename, mode="w", encoding=Writer.DEFAULT_ENCODING) as f:
            f.writelines(array)
        return array