from core.handlers.handler import AbstractHandler
from core.files.writer import Writer
import re

class Splitter(AbstractHandler):
    def __init__(self, limit=None):
        self.limit = limit

    def handle(self, request):
        result = self.split(request.getContent(), self.limit)

        Writer.write_iter("2_splitted.txt", self.beautify(result))
        print(f"SPLITED INTO {len(result)} chunks")
        request.setContent(self.toQueries(result))

        return super().handle(request)


    def split(self, pure, limit):
        if limit is None: raise Exception("Limit for splitting was not specified, abort")
        temp = [""]
        for line in pure.split("\n"):
            if len(temp[-1]) + len(line) > limit:
                temp.append(line+"\n")
            else:
                temp[-1] = temp[-1] + line + "\n"

        return temp

    def beautify(self, result):
        return "\n\n----\n\n".join(result)

    def toQueries(self, result):
        return [re.sub("\n", " ", line) for line in result]