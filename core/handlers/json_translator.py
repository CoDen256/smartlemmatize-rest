from core.handlers.handler import AbstractHandler
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


class TranslatorLTC(json.JSONEncoder):
    def __init__(self, fromContent, toContent):
        if fromContent == Content.JSON and toContent == Content.LTC:
            self.jsonToLtc= True
        elif fromContent == Content.LTC and toContent == Content.JSON:
            self.jsonToLtc = False
        else:
            raise Exception("Invalid arguments for target and source content")

    def translate(self, inputContent):
        if self.jsonToLtc:
            return self.translateFromJSON(inputContent)
        return self.translateToJSON(inputContent)

    def translateToJSON(self, ltc):
        return json.dumps(ltc, cls=LTCEncoder)

    def translateFromJSON(self, json):
        return json.loads(json)



class TranslatorPOS:

    def __init__(self, fromContent, toContent):
        if fromContent == Content.JSON and toContent == Content.POS:
            self.jsonToPos = True
        elif fromContent == Content.POS and toContent == Content.JSON:
            self.jsonToPos = False
        else:
            raise Exception("Invalid arguments for target and source content")

    def translate(self, inputContent):
        if self.jsonToPos:
            return self.translateFromJSON(inputContent)
        return self.translateToJSON(inputContent)

    def translateToJSON(self, pos):
        raise Exception("translateToJSON not implemented")

    def translateFromJSON(self, json_array):
        if (not isinstance(json_array, Iterable)):
            raise Exception("Failed to Merge JSON(POS), inputContent is not Iterable")
        
        result = []
        for response in json_array:
            sentences = response["body"]

            for sentence in sentences:
                res_sentence = []
                for lemma in sentence["tokens"]:
                    orig = lemma["text"]
                    main = lemma["moot"]["lemma"]
                    wType = lemma["moot"]["tag"]

                    res_sentence.append(PartOfSpeech(orig, main, wType))

                result.append(res_sentence)
        return result


