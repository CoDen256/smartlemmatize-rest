from abc import ABC, abstractmethod
from core.utils import assertType
from core.resource_manager import ResourceManager, Resource

class Handler(ABC):
    @abstractmethod
    def link(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass

class AbstractHandler(Handler):
    _linked = None

    def link(self, handler):
        self._linked = assertType("linkedHandler", handler, AbstractHandler)
        return handler

    @abstractmethod
    def handle(self, request):
        request.handledBy(type(self).__name__)
        return self.execute_linked(request)

    def execute_linked(self, request):
        if self._linked:
            return self._linked.handle(request)
        return request


class ResourceHandler(AbstractHandler):
    def __init__(self, manager, resource, onPresent, onAbsent):
        self._manager = assertType("manager", manager, ResourceManager)
        self._resource = assertType("resource", resource, Resource)

        self._onPresent = assertType("onPresentRootHandler", onPresent, AbstractHandler)
        self._onAbsent = assertType("onAbsentRootHandler", onAbsent, AbstractHandler)

    def handle(self, request):
        isPresent = self._manager.exists(self._resource, request)
        request.handledBy(type(self).__name__)

        print(f"Child deligation via {isPresent} condition from", type(self).__name__)

        if isPresent: return self._onPresent.handle(request)
        return self._onAbsent.handle(self.execute_linked(request))
