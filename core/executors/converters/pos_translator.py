from core.data.enums import Translators
from core.data.pos import PartOfSpeech
from collections.abc import Iterable


class TranslatorPOS:

    def __init__(self, from_content, to_content):
        if from_content == Translators.JSON and to_content == Translators.POS:
            self.jsonToPos = True
        elif from_content == Translators.POS and to_content == Translators.JSON:
            self.jsonToPos = False
        else:
            raise Exception("Invalid arguments for target and source content")

    def translate(self, input_content):
        if self.jsonToPos:
            return self.translate_from_json(input_content)
        return self.translate_to_json(input_content)

    def translate_to_json(self, pos):
        raise ValueError("Translation to JSON for POS not implemented")

    @staticmethod
    def translate_from_json(json_array):
        if not isinstance(json_array, Iterable):
            raise Exception("Failed to Merge JSON(POS), inputContent is not Iterable")

        result = []
        for json_response in json_array:
            sentences = json_response["body"]

            for sentence in sentences:
                res_sentence = []
                for lemma in sentence["tokens"]:
                    orig = lemma["text"]
                    main = lemma["moot"]["lemma"]
                    word_type = lemma["moot"]["tag"]

                    res_sentence.append(PartOfSpeech(orig, main, word_type))

                result.append(res_sentence)
        return result
