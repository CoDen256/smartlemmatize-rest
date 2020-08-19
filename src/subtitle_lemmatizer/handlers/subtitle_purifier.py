from .handler import AbstractHandler

class SubtitlePurifier(AbstractHandler):
    def handle(self, request):
        print("SubtitlePurifier handling the request "+str(request))

        request.remarks += "subtitlepurifier;"
        result = request

        return super().handle(result)