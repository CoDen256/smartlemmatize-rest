from abc import ABC, abstractmethod

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
        self._linked = handler
        return handler

    @abstractmethod
    def handle(self, request):
        return self.execute_linked(request)

    def execute_linked(self, request):
        if self._linked:
            return self._linked.handle(request)
        return request


class ParentHandler(AbstractHandler):
    _child1 = None
    _child2 = None

    def __init__(self, manager):
        self._manager = manager

    def set_condition(self, predicate, trueChild, falseChild):
        self._child1 = trueChild
        self._child2 = falseChild
        self._predicate = predicate

    def handle(self, request):
        if self._predicate(self._manager, request):
            print("Child deligation via true condition")
            return self._child1.handle(request)
        else:
            print("Child deligation via false condition")
            return self._child2.handle(self.execute_linked(request))