from core.handlers.abstract_handlers import AbstractHandler
from core.resource_manager import ResourceManager
from core.files.writer import Writer, ANY
from core.utils import logProcess

class ResourceSaver(AbstractHandler):
    def __init__(self, resource, content_type=ANY):
        self.resource = resource
        self.content_type = content_type

    def handle(self, request):
        logProcess("ResourceSaver saving...",  self.resource.name)

        path = ResourceManager.path(self.resource, request)
        
        request.setContent(Writer.write(path, request.getContent(), content_type=self.content_type))

        return super().handle(request)