import pprint

BYTE = "BYTE"
JSON = "JSON"
ANY = "ANY"

DEFAULT_ENCODING = "utf-8-sig"

class Writer:

    @staticmethod
    def write(filename, content, content_type=ANY):
        if content_type == BYTE:
            return Writer.write_bin(filename, content)
        elif content_type == ANY:
            return Writer.write_text(filename, content)
        elif content_type == JSON:
            return Writer.write_text(filename, content, pretty=False)
        
        raise Exception("Undentified content type")

    @staticmethod
    def write_text(filename, content, pretty=True):
        print("[Wrtiting text to ", filename, "]")
        with open(filename, mode="w", encoding=DEFAULT_ENCODING) as f:
            if pretty:
                f.write(pprint.pformat(content))
            else:
                f.write(content)
        return content
    
    @staticmethod
    def write_bin(filename, content):
        print("[Wrtiting binary to ", filename, "]")
        with open(filename, mode="wb") as f:
            f.write(content)
            
        return content.decode(encoding=DEFAULT_ENCODING).replace("\r", "")

    @staticmethod
    def write_custom(filename, content, **kwargs):
        #print("[Wrtiting custom to ", filename, "]")
        with open(filename, **kwargs) as f:
            f.write(content)
        return content