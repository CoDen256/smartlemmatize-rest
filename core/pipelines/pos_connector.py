from core.pipelines.abc.abstract_pipeline import Pipeline
from core.executors.lemmatization.connector import LemmaConnector
from core.data.pos import PartOfSpeech


class PosConnector(Pipeline):
    def __init__(self):
        super().__init__()

    def execute(self, incoming_data):
        pos_list = incoming_data.get('data')
        assert isinstance(pos_list, list)
        assert isinstance(pos_list[0], list)
        assert isinstance(pos_list[0][0], PartOfSpeech)

        connector = LemmaConnector()

        self.submit(pos_list=connector.connect(pos_list))
