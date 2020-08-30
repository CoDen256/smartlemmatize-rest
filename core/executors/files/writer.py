import pprint
from core.data.enums import Files

printer = pprint.PrettyPrinter(width=2000)


class Writer:
    @staticmethod
    def write(filename, content, enc, content_type=Files.RAW):
        if content_type == Files.BYTE:
            return Writer.write_byte(filename, content)
        elif content_type == Files.RAW:
            return Writer.write_raw(filename, content, enc, pretty=False)
        elif content_type == Files.PRETTY:
            return Writer.write_raw(filename, content, enc, pretty=True)

        raise TypeError("Undefined content type")

    @staticmethod
    def write_raw(filename, content, enc, pretty):
        print("[Writing text to ", filename, "]")
        with open(filename, mode="w", encoding=enc, newline='') as f:
            if pretty:
                f.write(printer.pformat(content))
            else:
                f.write(str(content))
        return content

    @staticmethod
    def write_byte(filename, content):
        if not isinstance(content, bytes):
            raise TypeError("Content is not byte")
        print("[Writing binary to ", filename, "]")
        with open(filename, mode="wb") as f:
            f.write(content)

        return content

    @staticmethod
    def write_custom(filename, content, **kwargs):
        kwargs['newline'] = ''
        with open(filename, **kwargs) as f:
            f.write(content)
        return content