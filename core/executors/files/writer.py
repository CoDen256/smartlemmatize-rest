import pprint
from core.data.enums import Files

class Writer:

    @staticmethod
    def write(filename, content, content_type=Files.RAW):
        if content_type == Files.BYTE:
            return Writer.write_bin(filename, content)
        elif content_type == Files.RAW:
            return Writer.write_text(filename, content, pretty=False)
        elif content_type == Files.PRETTY:
            return Writer.write_text(filename, content, pretty=True)

        raise Exception("Undefined content type")

    @staticmethod
    def write_text(filename, content, pretty=True):
        print("[Writing text to ", filename, "]")
        with open(filename, mode="w", encoding=Files.DEFAULT_ENCODING) as f:
            if pretty:
                f.write(pprint.pformat(content))
            else:
                f.write(content)
        return content
    
    @staticmethod
    def write_bin(filename, content):
        print("[Writing binary to ", filename, "]")
        with open(filename, mode="wb") as f:
            f.write(content)
            
        return content

    @staticmethod
    def write_custom(filename, content, **kwargs):
        with open(filename, **kwargs) as f:
            f.write(content)
        return content