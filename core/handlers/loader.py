from core.handlers.abstract_handlers import AbstractHandler
from core.resource_manager import ResourceManager
from core.executors.files.reader import Reader
from core.utils import logProcess

class ResourceLoader(AbstractHandler):
    def __init__(self, resource):
        self.resource = resource

    def handle(self, request):
        logProcess("ResourceLoader loading...", self.resource.name)

        path = ResourceManager.path(self.resource, request)

        request.setContent(Reader.read_text(path))

        return super().handle(request)