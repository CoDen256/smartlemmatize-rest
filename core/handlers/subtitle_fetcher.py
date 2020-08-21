from core.handlers.handler import AbstractHandler
from core.files.writer import Writer

class SubtitleFetcher(AbstractHandler):
    def handle(self, request):
        result = request.getContent()

        request.setContent(result)

        return super().handle(request)