from core.executors.files.writer import Writer

def log_process(*info):
    print(*info)
    Writer.write_custom("log/process_log.txt", (" ".join([str(i) for i in info]) + '\n'),
                        mode="a", encoding='utf-8')
