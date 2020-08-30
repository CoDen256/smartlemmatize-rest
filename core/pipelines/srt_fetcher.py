from core.pipelines.abc.abstract_pipeline import Pipeline
from core.executors.web_services.open_subtitle_service import OpenSubtitleService
from core.data.request import Request


class SubtitleFetcher(Pipeline):
    def execute(self, incoming_data):
        request = incoming_data.get('request')
        assert isinstance(request, Request)

        result, encoding = OpenSubtitleService.fetch(request)

        request.setEncoding(encoding)

        self.submit(gzip=result, encoding=encoding)
