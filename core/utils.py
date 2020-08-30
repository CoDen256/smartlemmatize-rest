from core.executors.files.writer import Writer
from core.data.enums import Files

def log_process(*info):
    print(*info)
    Writer.write_custom("log/process_log.txt", (" ".join([str(i) for i in info]) + '\n'),
                        mode="a", encoding=Files.DEFAULT_ENCODING)
