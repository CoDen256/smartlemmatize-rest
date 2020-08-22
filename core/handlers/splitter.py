from core.handlers.abstract_handlers import AbstractHandler
from core.utils import log, logProcess
import re

class Splitter(AbstractHandler):
    def __init__(self, limit=None, decapitalize=False):
        self.limit = limit
        self.decapitalize = decapitalize

    def handle(self, request):
        result = self.split(request.getContent(), self.limit)

        log("3_splitted.txt", self.beautify(result))

        logProcess(f"SPLITED INTO {len(result)} chunks")

        request.setContent(self.toQueries(result))

        return super().handle(request)


    def split(self, pure, limit):
        if limit is None: raise Exception("Limit for splitting was not specified, abort")
        temp = [""]
        for line in pure.split("\n"):
            result_line = line.strip()
            if len(result_line) <= 1: continue

            if self.decapitalize:
                result_line = result_line[0].lower() + result_line[1:]

            if len(temp[-1]) + len(result_line) > limit:
                temp.append(result_line+"\n")
            else:
                temp[-1] = temp[-1] + result_line + "\n"

        return temp

    def beautify(self, result):
        return "\n\n----\n\n".join(result)

    def toQueries(self, result):
        return [re.sub("\n", " ", line) for line in result]