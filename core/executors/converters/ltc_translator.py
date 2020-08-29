import json
from core.data.enums import Translators


class TranslatorLTC(json.JSONEncoder):
    def __init__(self, from_content, to_content):
        super().__init__()
        if from_content == Translators.JSON and to_content == Translators.LTC:
            self.jsonToLtc = True
        elif from_content == Translators.LTC and to_content == Translators.JSON:
            self.jsonToLtc = False
        else:
            raise Exception("Invalid arguments for target and source content")

    def translate(self, input_content):
        if self.jsonToLtc:
            return TranslatorLTC.translate_from_json(input_content)
        return TranslatorLTC.translate_to_json(input_content)

    @staticmethod
    def translate_to_json(ltc_array):
        return json.dumps(ltc_array, cls=LtcEncoder)

    @staticmethod
    def translate_from_json(json_ltc):
        raise ValueError("Translation from json for LTC not implemented")

    def default(self, o):
        return o.__dict__


class LtcEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
