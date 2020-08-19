from core.handlers.handler import ResourceHandler
from core.resource_manager import ResourceManager

class SRTProvider(ResourceHandler):
    def __init__(self, manager, trueChild, falseChild):
        self.resource = manager.SRT
        super().__init__(manager, self.resource,
                         trueChild, falseChild)