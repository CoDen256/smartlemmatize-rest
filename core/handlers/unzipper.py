from core.handlers.handler import AbstractHandler
from core.files.writer import Writer
import os
import gzip
import shutil

class Unzipper(AbstractHandler):
    def handle(self, request):
        result = self.unzip(request.getContent())

        request.setContent(result)
        
        Writer.write_bin("01_unzipped.srt", result)

        return super().handle(request)

    def unzip(self, data):
        return gzip.decompress(data)