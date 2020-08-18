from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def set_child(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass

class AbstractHandler(Handler):
    _next_child = None

    def set_next(self, handler):
        self._next_child = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_child:
            return self._next_child.handle(request)

        return None