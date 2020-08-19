from handlers import AbstractHandler
from subtitle_lemmatizer import ResourceManager

class Loader(AbstractHandler):
    def __init__(self, resource):
        self.resource = resource

    def handle(self, request):
        print("Loader handling the request",  request)

        path = ResourceManager.path(self.resource, request)

        with open(path, mode="r", encoding='utf-8-sig') as f:
            request.setContent(f.read())

        return super().handle(request)