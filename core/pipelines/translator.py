from core.pipelines.abc import Pipeline
from core.executors.converters.pos_translator import TranslatorPOS
from core.executors.converters.ltc_translator import TranslatorLTC
from core.data.enums import Translators
from core.utils import log_process


class Translator(Pipeline):

    def __init__(self, from_content, to_content):
        super().__init__()
        if from_content not in Translators.ALL: raise Exception("Source content is undefined")
        if to_content not in Translators.ALL: raise Exception("Target content is undefined")

        self.from_content = from_content
        self.to_content = to_content

    def execute(self, incoming_data):
        data = incoming_data.get('data')
        assert isinstance(data, list)

        translator = self.get_translator()

        log_process(f"Translating with {type(translator).__name__}")

        self.submit(data=translator.translate(data))

    def get_translator(self):
        if Translators.LTC in [self.from_content, self.to_content]:
            return TranslatorLTC(self.from_content, self.to_content)
        if Translators.POS in [self.from_content, self.to_content]:
            return TranslatorPOS(self.from_content, self.to_content)
