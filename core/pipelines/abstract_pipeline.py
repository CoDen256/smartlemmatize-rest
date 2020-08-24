from abc import ABC, abstractmethod
from core.pipelines.pipeline_data import PipelineData


class AbstractReceiver(ABC):
    def __init__(self):
        self._incoming_pipelines = []
        self._inputs = {}

    def from_(self, *pipelines):
        for p in pipelines:
            assert isinstance(p, AbstractSubmitter)
            p.connect_to(self)
            self.connect_from(p)

        return self

    def connect_from(self, pipeline):
        assert isinstance(pipeline, AbstractSubmitter)
        self._incoming_pipelines.append(pipeline)

    def receive(self, pipeline, input):
        assert isinstance(pipeline, AbstractSubmitter)
        assert isinstance(input, dict)

        self._inputs[pipeline] = input

        if all([p.is_finished() for p in self._incoming_pipelines]):
            self.check_and_execute(PipelineData(self._inputs))

    def check_and_execute(self, incoming_data):
        assert isinstance(incoming_data, PipelineData)
        try:
            self.execute(incoming_data)
        except Exception as e:
            raise PipelineExecutionException(self, e)

    @abstractmethod
    def execute(self, incoming_data):
        """
        :param incoming_data: incoming data, must be PipelineInput
        must call self.finish(**data)
        """
        pass


class AbstractSubmitter(ABC):
    def __init__(self):
        self._outcoming_pipelines = []
        self._own_output = None

    def to(self, *pipelines):
        for p in pipelines:
            assert isinstance(p, AbstractReceiver)
            self.connect_to(p)
            p.connect_from(self)
        return self

    def connect_to(self, pipeline):
        assert isinstance(pipeline, AbstractReceiver)
        self._outcoming_pipelines.append(pipeline)

    def submit(self, **own_output):
        self.set_output(own_output)
        for pipeline in self._outcoming_pipelines:
            assert isinstance(pipeline, AbstractReceiver)
            pipeline.receive(self, own_output)

    def set_output(self, own_output):
        assert isinstance(own_output, dict)
        self._own_output = own_output

    def get_output(self):
        return self._own_output

    def is_finished(self):
        return bool(self.get_output())


class Pipeline(AbstractReceiver, AbstractSubmitter):
    @abstractmethod
    def execute(self, incoming_data):
        pass


class PipelineExecutionException(Exception):
    def __init__(self, pipeline, cause, *args):
        super().__init__(*args)
        self.pipeline = pipeline
        self.cause = cause
