from core.handlers.handler import ResourceHandler
from core.resource_manager import ResourceManager

class LTCProvider(ResourceHandler):
    def __init__(self, manager, trueChild, falseChild):
        self.resource = manager.LTC
        super().__init__(manager, self.resource,
                         trueChild, falseChild)