from core.pipelines.abc.abstract_pipeline import Pipeline
from core.executors.files.unzipper import Gzipper


class SrtUnzipper(Pipeline):
    def execute(self, incoming_data):
        data = incoming_data.get('gzip')
        assert data is not None
        # TODO is byte

        gzipper = Gzipper()

        self.submit(data=gzipper.unzip(data))
