from .handler import AbstractHandler

class JSONTranslator(AbstractHandler):
    def handle(self, request):
        print("JSONTranslator handling the request "+str(request))

        request.remarks += "jsontranslator;"
        result = request


        return super().handle(result)