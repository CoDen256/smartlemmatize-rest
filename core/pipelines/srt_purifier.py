from core.pipelines.abc import Pipeline
from core.executors.converters.purifier import Purifier
from core.utils import log_process


class SrtPurifier(Pipeline):

    def __init__(self, stages):
        super().__init__()
        self.stages = stages

    def execute(self, incoming_data):
        srt = incoming_data.get('srt')
        assert isinstance(srt, str)

        purifier = Purifier(self.stages)

        log_process("Purifying... with stages:", self.stages)

        self.submit(pure=purifier.apply(srt))
