from core.handlers.handler import AbstractHandler
from core.resource_manager import ResourceManager
from core.files.writer import Writer

class ResourceSaver(AbstractHandler):
    def __init__(self, resource, **kwargs):
        self.resource = resource
        self.kwargs = kwargs

    def handle(self, request):
        print("ResourceSaver saving...",  self.resource.name)

        path = ResourceManager.path(self.resource, request)

        writer = Writer(**self.kwargs)
        writer.write(path, request.getContent())

        return super().handle(request)