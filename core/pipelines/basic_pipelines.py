from core.pipelines.abstract_pipeline import Pipeline, AbstractSubmitter, AbstractReceiver, PipelineExecutionException
from core.pipelines.pipeline_data import PipelineData, PipelineDataException
from abc import ABC, abstractmethod


class VoidPipeline(Pipeline):
    """
    Just executes some task on input, without changing the input
    """
    def execute(self, incoming_data):
        self.run(incoming_data)
        self.submit(**incoming_data.get_data())

    @abstractmethod
    def run(self, incoming_data):
        pass


class Starter(AbstractSubmitter):
    """
    Starts the execution of pipeline from the given input
    """
    def __init__(self, **start_data):
        super().__init__()
        self.start_data = start_data

    def start(self):
        self.submit(**self.start_data)


class Finisher(AbstractReceiver):
    """
    Finishes the execution of pipeline and returns result value
    """
    def __init__(self):
        super().__init__()
        self.result_data = None

    def get_result(self):
        return self.result_data

    def execute(self, incoming_data):
        self.result_data = incoming_data
