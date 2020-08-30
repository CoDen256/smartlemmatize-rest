from core.pipelines.abc import Pipeline
from core.executors.files import Decoder


class SrtDecoder(Pipeline):
    def __init__(self):
        super().__init__()

    def execute(self, incoming_data):
        data = incoming_data.get('data')
        encoding = incoming_data.get('encoding')
        assert isinstance(data, bytes)

        self.submit(srt=Decoder(encoding).decode(data))
