from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass

class AbstractHandler(Handler):
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        pass

    def execute_next(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)

class IntermediateHandler(AbstractHandler):
    @abstractmethod
    def handle(self, request):

        pass
class TerminalHandler(AbstractHandler):
    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)

        return None

class ParentHandler(AbstractHandler):
    _child1 = None
    _child2 = None

    def __init__(self, manager):
        self._manager = manager

    def set_condition(self, predicate, child1, child2):
        self._child1 = child1
        self._child2 = child2
        self._predicate = predicate

    def handle(self, request):
        processed = None
        if self._predicate(self._manager):
            processed = self._child1.handle(request)
        else:
            processed = self._child2.handle(request)
        return super.handle(processed)