from .handler import AbstractHandler

class TimeStamper(AbstractHandler):
    def handle(self, request):
        print("TimeStamper handling the request "+str(request))

        request.remarks += "timestamper;"
        result = request


        return super().handle(result)