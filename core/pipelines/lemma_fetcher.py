from core.pipelines.abc import Pipeline
from core.executors.web_services.cab_web_service import CabWebService


class LemmaFetcher(Pipeline):

    def __init__(self):
        super().__init__()

    def execute(self, incoming_data):
        chunks = incoming_data.get('chunks')
        assert isinstance(chunks, list)

        lemmata = CabWebService.fetch(chunks)

        self.submit(data=lemmata)
