from core.handlers.handler import AbstractHandler
from core.resource_manager import ResourceManager

class Saver(AbstractHandler):
    def __init__(self, resource):
        self.resource = resource

    def handle(self, request):
        print("ResourceSaver saving...",  self.resource.name)

        path = ResourceManager.path(self.resource, request)

        with open(path, mode="w", encoding='utf-8-sig') as f:
            f.write(request.getContent())

        return super().handle(result)