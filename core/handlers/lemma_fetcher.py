from core.handlers.handler import AbstractHandler
from core.services.cab_web_service import CabWebService
from core.utils import log

class LemmaFetcher(AbstractHandler):
    def handle(self, request):

        result = CabWebService.fetch(request.getContent())

        request.setContent(result)
        log("4_cabweb.json", result)


        return super().handle(request)