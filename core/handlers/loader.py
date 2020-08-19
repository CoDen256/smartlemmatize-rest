from core.handlers.handler import AbstractHandler
from core.resource_manager import ResourceManager
from core.files.reader import Reader

class ResourceLoader(AbstractHandler):
    def __init__(self, resource):
        self.resource = resource

    def handle(self, request):
        print("ResourceLoader loading...", self.resource.name)

        path = ResourceManager.path(self.resource, request)

        request.setContent(Reader.read_text(path))

        return super().handle(request)