from core.handlers.abstract_handlers import AbstractHandler
from core.utils import log
from core.data import LemmatizedTimeCode, PartOfSpeech, LTCEncoder
import json
from collections.abc import Iterable

class Content:
    JSON = "JSON"
    LTC = "LTC"
    POS = "POS"
    CONTENTS = [JSON, LTC, POS]


    @staticmethod
    def getTranslator(fromContent, toContent):
        if Content.LTC in [fromContent, toContent]:
            return TranslatorLTC(fromContent, toContent)
        elif Content.POS in [fromContent, toContent]:
            return TranslatorPOS(fromContent, toContent)
        else:
            raise Exception("Invalid contents")

class JSONTranslator(AbstractHandler):

    def __init__(self, fromContent, toContent):
        if fromContent not in Content.CONTENTS: raise Exception("Source content is undefined")
        if toContent not in Content.CONTENTS: raise Exception("Target content is undefined")

        self.fromContent = fromContent
        self.toContent = toContent

    def handle(self, request):

        translator = Content.getTranslator(self.fromContent, self.toContent)

        result = translator.translate(request.getContent())

        request.setContent(result)

        log(f"9_json_translator{self.fromContent}_{self.toContent}.txt", result)
        return super().handle(request)



