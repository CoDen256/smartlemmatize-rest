from core.pipelines.abc import Pipeline
from core.resource_manager import ResourceManager
from core.data.request import Request
from core.executors.files.reader import Reader
from core.utils import log_process


class ResourceLoader(Pipeline):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def execute(self, incoming_data):
        request = incoming_data.get('request')

        assert isinstance(request, Request)

        log_process("ResourceLoader loading...", self.resource.name)

        path = ResourceManager.path(self.resource, request)

        self.submit(srt=Reader.read_raw(path, enc=request.encoding))
