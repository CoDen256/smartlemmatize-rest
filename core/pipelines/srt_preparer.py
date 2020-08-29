from core.pipelines.abc import Pipeline
from core.executors.converters.preparer import Preparer
from core.utils import log_process


class SrtPreparer(Pipeline):

    def __init__(self, limit, decapitalize):
        super().__init__()
        self.limit = limit
        self.decapitalize = decapitalize

    def execute(self, incoming_data):
        pure = incoming_data.get('pure')
        assert isinstance(pure, list)
        assert isinstance(pure[0], str)

        preparer = Preparer(self.limit, decapitalize=self.decapitalize)
        chunks = preparer.split_and_prepare(pure)

        log_process(f"Prepared {len(chunks)} chunks")

        self.submit(chunks=chunks)
