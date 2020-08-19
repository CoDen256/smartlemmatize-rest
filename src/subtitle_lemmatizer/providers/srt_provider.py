from ..handler import ParentHandler
from ..resources.resource_manager import ResourceManager

class SRTProvider(ParentHandler):
    def __init__(self, manager, trueChild, falseChild):
        super().__init__(manager)
        self.set_condition(
            lambda m, q: m.resource_exists(ResourceManager.SRT, q) != None,
            trueChild,
            falseChild
        )