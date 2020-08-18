from .handler import AbstractHandler

class Reader(AbstractHandler):
    def handle(self, request):
        print("Reader handles request",  request)

        return super.handle(request)