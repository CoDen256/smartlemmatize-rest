from core.pipelines.abc import VoidPipeline
from core.executors.files.writer import Writer
from core.resource_manager import ResourceManager
from core.utils import log_process


class ResourceSaver(VoidPipeline):
    def __init__(self, resource, content_type):
        super().__init__()
        self.resource = resource
        self.content_type = content_type

    def run(self, incoming_data):
        request = incoming_data.get('request')
        data = incoming_data.get('data')

        log_process("ResourceSaver saving...", self.resource.name)

        path = ResourceManager.path(self.resource, request)

        Writer.write(path, data, content_type=self.content_type)

