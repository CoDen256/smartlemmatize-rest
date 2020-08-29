from abc import ABC, abstractmethod
from core.pipelines.abc.pipeline_data import PipelineData, PipelineDataException
from core.pipelines.abc.group import PipelineSubmitterGroup, PipelineReceiverGroup


class AbstractReceiver(ABC):
    def __init__(self):
        self.incoming_pipelines = []
        self.inputs = {}

    def from_(self, *pipelines):
        for p in pipelines:
            self.check_in(p)
            p.connect_to(self)
            self.connect_from(p)

        return PipelineReceiverGroup(pipelines)

    def check_in(self, pipeline):
        if not isinstance(pipeline, AbstractSubmitter) or pipeline == self:
            self.disconnect()
            raise PipelineConnectionException(pipeline, self)

    def connect_from(self, pipeline):
        assert isinstance(pipeline, AbstractSubmitter)
        self.incoming_pipelines.append(pipeline)

    def receive(self, pipeline, input):
        assert isinstance(pipeline, AbstractSubmitter)
        assert isinstance(input, dict)

        self.inputs[pipeline] = input

        if all([p.is_finished() and p in self.inputs.keys() for p in self.incoming_pipelines]):
            self.check_and_execute(PipelineData(self.inputs))

    def check_and_execute(self, incoming_data):
        assert isinstance(incoming_data, PipelineData)
        try:
            self.execute(incoming_data)
        except PipelineDataException as e_data:
            raise e_data
        except Exception as e:
            raise PipelineExecutionException(self, e)

    def disconnect(self):
        self.incoming_pipelines = []
        self.inputs = None

    @abstractmethod
    def execute(self, incoming_data):
        """
        :param incoming_data: incoming data, must be PipelineInput
        must call self.finish(**data)
        """
        pass

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"{type(self).__name__}" \
               f"({str([s.__str__() for s in self.incoming_pipelines])})"


class AbstractSubmitter(ABC):
    def __init__(self):
        self.outcoming_pipelines = []
        self.own_output = None

    def to(self, *pipelines):
        for p in pipelines:
            self.check_out(p)
            self.connect_to(p)
            p.connect_from(self)

        return PipelineSubmitterGroup(pipelines)

    def check_out(self, pipeline):
        if not isinstance(pipeline, AbstractReceiver) or pipeline == self:
            self.disconnect()
            raise PipelineConnectionException(self, pipeline)

    def connect_to(self, pipeline):
        assert isinstance(pipeline, AbstractReceiver)
        self.outcoming_pipelines.append(pipeline)

    def submit(self, **own_output):
        self.set_output(own_output)
        for pipeline in self.outcoming_pipelines:
            assert isinstance(pipeline, AbstractReceiver)
            pipeline.receive(self, own_output)

    def disconnect(self):
        self.outcoming_pipelines = []
        self.own_output = None

    def set_output(self, own_output):
        assert isinstance(own_output, dict)
        self.own_output = own_output

    def get_output(self):
        return self.own_output

    def is_finished(self):
        return bool(self.get_output())

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"{type(self).__name__}" \
               f"({str([s.__str__() for s in self.outcoming_pipelines])})"


class Pipeline(AbstractReceiver, AbstractSubmitter):
    def __init__(self):
        AbstractReceiver.__init__(self)
        AbstractSubmitter.__init__(self)

    def disconnect(self):
        AbstractReceiver.disconnect(self)
        AbstractSubmitter.disconnect(self)

    @abstractmethod
    def execute(self, incoming_data):
        pass


    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"{type(self).__name__}" \
               f"({str([s.__str__() for s in self.incoming_pipelines])}" \
               f"{str([s.__str__() for s in self.outcoming_pipelines])})"


class PipelineConnectionException(Exception):
    def __init__(self, source, target, *args):
        super().__init__(f"Cannot connect {type(source).__name__} to {type(target).__name__}", *args)
        self.source = source
        self.target = target


class PipelineExecutionException(Exception):
    def __init__(self, pipeline, cause, *args):
        super().__init__(*args)
        self.pipeline = pipeline
        self.cause = cause
