from .handler import AbstractHandler

class SubtitleFetcher(AbstractHandler):
    def handle(self, request):
        print("SubtitleFetcher handling the request "+str(request))

        return super.handle(request) 