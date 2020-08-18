from ..handler import ParentHandler

class SRTProvider(ParentHandler):
    _child1 = None
    _child2 = None

    def __init__(self, manager):
        self._manager = manager

    def set_condition(self, predicate, child1, child2):
        self._child1 = child1
        self._child2 = child2
        self._predicate = predicate

    def handle(self, request):
        if self._predicate(self._manager):
            self._child1.handle(request)
        else:
            self._child2.handle(request)
        return super.handle()