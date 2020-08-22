from core.handlers.handler import AbstractHandler
from core.utils import log
from core.files import BYTE
from core.services.open_subtitle_service import OpenSubtitleService

class SubtitleFetcher(AbstractHandler):
    def handle(self, request):
        result = OpenSubtitleService.fetch(request)

        request.setContent(result)

        return super().handle(request)