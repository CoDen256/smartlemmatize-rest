from handlers import AbstractHandler

class LemmaFetcher(AbstractHandler):
    def handle(self, request):
        print("LemmaFetcher handling the request "+str(request))

        request.remarks += "lemmafetcher;"
        result = request


        return super().handle(result)