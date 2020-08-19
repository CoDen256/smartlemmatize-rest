from handlers import AbstractHandler
from subtitle_lemmatizer import ResourceManager

class Saver(AbstractHandler):
    def __init__(self, resource):
        self.resource = resource

    def handle(self, request):
        print("Saver handling the request",  request)

        path = ResourceManager.path(self.resource, request)

        with open(path, mode="w", encoding='utf-8-sig') as f:
            f.write(request.getContent())

        return super().handle(result)