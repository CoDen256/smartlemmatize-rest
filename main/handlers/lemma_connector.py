from .handler import AbstractHandler

class LemmaConnector(AbstractHandler):
    def handle(self, request):
        print("LemmaConnector handling the request "+str(request))

        request.remarks += "lemmaconnector;"
        result = request


        return super().handle(result)