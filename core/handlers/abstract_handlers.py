from abc import ABC, abstractmethod
from core.utils import assertType, logProcess
from core.resource_manager import ResourceManager, Resource
from core.data import Request
from core.executors import Executor


# TODO REDESIGN CONCEPT TO PIPELINES
# pipe -> pipe1 -> pipe2 -> pipe3
# pipe -> pipe3(will start executing only when will get result from all incoming pipelines)
# conditional pipe
# configuring their connections from the beginning
# raise PipelineExceptions
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
        self._linked = assertType("Abstract.link(!handler)", handler, AbstractHandler)
        return handler

    @abstractmethod
    def handle(self, request):
        assertType("Abstract.handle(!request)", request, Request)
        request.handledBy(type(self).__name__)
        return self.execute_linked(request)

    def execute_linked(self, request):
        if self._linked:
            return self._linked.handle(request)
        return request


class ExecutionHandler(AbstractHandler, ABC):
    def __init__(self, executor):
        self.executor = assertType("ExecutionHandler.executor", executor, Executor)

    def handle(self, request):
        assertType("ExecutionHandler.request", request, Request)
        if not self.check_input(request):
            raise Exception(f"Check of Input aborted for {type(self).__name__}")

        result = self.executor.execute(request)

        if not self.check_output(request):
            raise Exception(f"Check for Output aborted for {type(self).__name__}")
        request.setContent(result)

        return super().handle(request)

    @abstractmethod
    def check_input(self, input_request):
        pass

    @abstractmethod
    def check_output(self, output_request):
        pass


class ResourceHandler(AbstractHandler):
    def __init__(self, manager, resource, on_present, on_absent):
        self._manager = assertType("ResourceHandler.manager", manager, ResourceManager)
        self._resource = assertType("ResourceHandler.resource", resource, Resource)

        self._onPresent = assertType("ResourceHandler.onPresent", on_present, AbstractHandler)
        self._onAbsent = assertType("ResourceHandler.onAbsent", on_absent, AbstractHandler)

    def handle(self, request):
        is_present = self._manager.exists(self._resource, request)
        request.handledBy(type(self).__name__)

        logProcess(f"Child delegation via {is_present} condition from", type(self).__name__)

        if is_present:
            return self._onPresent.handle(request)
        return self._onAbsent.handle(self.execute_linked(request))
