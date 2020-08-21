from core.handlers.handler import AbstractHandler

class LemmaFetcher(AbstractHandler):
    def handle(self, request):
        result = request

        print(request.getContent())


        return super().handle(result)