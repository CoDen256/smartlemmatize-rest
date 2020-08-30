from core.pipelines.abc import Pipeline
from core.executors.files import Decoder


class SrtDecoder(Pipeline):
    def __init__(self, encoding):
        super().__init__()
        self.encoding = encoding

    def execute(self, incoming_data):
        data = incoming_data.get('data')

        assert isinstance(data, bytes)

        self.submit(srt=Decoder(self.encoding).decode(data))
