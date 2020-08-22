from core.executors.files.writer import Writer

BYTE, RAW, PRETTY = 1, 2, 4
DEFAULT_ENCODING = "utf-8-sig"


def assert_type(context, current, expected):
    if not isinstance(current, expected) or current is None:
        raise TypeError(f"{context} expected to be {expected.__name__} but got {type(current).__name__}")
    return current


def log(source, info, content_type=RAW):
    dest = "log/" + source
    Writer.write(dest, info, content_type)


def log_process(*info):
    print(*info)
    Writer.write_custom("log/process_log.txt", (" ".join([str(i) for i in info]) + '\n'),
                        mode="a", encoding=DEFAULT_ENCODING)
