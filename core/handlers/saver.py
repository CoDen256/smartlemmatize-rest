from core.handlers.handler import AbstractHandler
from core.resource_manager import ResourceManager
from core.files.writer import Writer

class ResourceSaver(AbstractHandler):
    def __init__(self, resource):
        self.resource = resource

    def handle(self, request):
        print("ResourceSaver saving...",  self.resource.name)

        path = ResourceManager.path(self.resource, request)

        Writer.write_text(path, request.getContent())

        return super().handle(result)