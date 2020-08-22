from core.handlers.handler import AbstractHandler
from core.files.writer import Writer
from core.services.open_subtitle_service import OpenSubtitleService

class SubtitleFetcher(AbstractHandler):
    def handle(self, request):
        result = OpenSubtitleService.fetch(request)

        request.setContent(result)
        Writer.write_bin("0_subtitles.gz", result)

        return super().handle(request)