from core.pipelines.abc.abstract_pipeline import Pipeline
from core.executors.lemmatization.allocator import Allocator
from core.data.pos import PartOfSpeech


class LtcAllocator(Pipeline):
    def __init__(self):
        super().__init__()

    def execute(self, incoming_data):
        pos_list = incoming_data.get('pos_list')
        pure = incoming_data.get('pure')
        assert isinstance(pos_list, list)
        assert isinstance(pos_list[0], PartOfSpeech)
        assert isinstance(pure, list)

        allocator = Allocator()

        self.submit(data=allocator.allocate(pure, pos_list))
