from core.handlers.handler import AbstractHandler
from core.services.cab_web_service import CabWebService
from core.files.writer import Writer

class LemmaFetcher(AbstractHandler):
    def handle(self, request):

        result = CabWebService.fetch(request.getContent())

        request.setContent(result)
        Writer.write_iter("3_cabweb.txt", [str(r) for r in result])


        return super().handle(request)