from core.handlers.abstract_handlers import AbstractHandler
from core.executors.web_services import OpenSubtitleService

class SubtitleFetcher(AbstractHandler):
    def handle(self, request):
        result = OpenSubtitleService.fetch(request)

        request.setContent(result)

        return super().handle(request)