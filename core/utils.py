from datetime import datetime
from core.files.writer import Writer, ANY, DEFAULT_ENCODING

def assertType(context, current, expected):
    if not isinstance(current, expected):
        raise Exception(f"{context} expected to be {expected.__name__} but got {type(current).__name__}")
    return current

def log(source, info, content_type=ANY):
    dest = "log/"+source
    Writer.write(dest, info, content_type)

def logProcess(*info):
    print(*info)
    Writer.write_custom("log/process_log.txt", (" ".join([str(i) for i in info])+'\n'), 
                mode="a", encoding=DEFAULT_ENCODING)