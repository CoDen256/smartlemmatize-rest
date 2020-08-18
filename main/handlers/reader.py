from .handler import AbstractHandler

class Reader(AbstractHandler):
    def handle(self, request):
        print("Reader handling the request",  request)

        request.remarks += "reader;"
        result = request


        return super().handle(result)