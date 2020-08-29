from core.handlers.abstract_handlers import AbstractHandler
from core.utils import log
from core.files import BYTE
import gzip

class Unzipper(AbstractHandler):
    def handle(self, request):
        result = self.unzip(request.getContent())

        request.setContent(result)
        
        log("1_unzipped.srt", result, BYTE)

        return super().handle(request)

    def unzip(self, data):
        return gzip.decompress(data)