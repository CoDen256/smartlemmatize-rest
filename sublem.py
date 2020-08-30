from core.utils import log_process
from core.data import Request
from core.data.enums import Files, PureCodes, Constants, Translators
from core.resource_manager import ResourceManager
from core.pipelines import *


class SubtitleLemmatizer:
    # imdb_id - id of movie on imdb.  https://www.imdb.com/  => search => url ../title/tt{ID}/...
    # season - season of movie
    # episode - episode of movie

    def lemmatize(self, request):
        assert isinstance(request, Request)
        manager = ResourceManager()

        starter = Starter(request=request)
        finisher = Finisher()
        connector = Connector()

        connector.add_connection("NO_SRT", self.create_srt)
        connector.add_connection("NO_LTC", self.create_ltc)
        connector.add_connection("ALL", self.load_ltc)

        if not manager.exists(ResourceManager.SRT, request):
            starter, finisher, last = connector.connect("NO_SRT", starter, finisher, None)
            connector.connect("NO_LTC", starter, finisher, last)
        elif not manager.exists(ResourceManager.LTC, request):
            connector.connect("NO_LTC", starter, finisher, starter.to(ResourceLoader(ResourceManager.SRT)))
        else:
            connector.connect("ALL", starter, finisher, None)
        # connector.connect("NO_LTC")
        starter.start()

        return finisher.result_data

    def create_srt(self, starter, finisher, last):
        fetcher_srt = SubtitleFetcher()
        unzipper_srt = SrtUnzipper()
        saver_srt = ResourceSaver(ResourceManager.SRT, Files.BYTE)
        decoder_srt = SrtDecoder()

        starter.to(saver_srt)
        starter.to(fetcher_srt).to(unzipper_srt).to(saver_srt).to(decoder_srt)
        return starter, finisher, decoder_srt

    def create_ltc(self, starter, finisher, srt_provider):  # either decoder, or loader
        purifier_srt = SrtPurifier(PureCodes.ALL)
        purifier_parse = SrtPurifier(PureCodes.DEFAULT | PureCodes.PARSE)
        preparer_srt = SrtPreparer(Constants.MAX_LENGTH, decapitalize=True)
        fetcher = LemmaFetcher()
        translator_json_pos = Translator(Translators.JSON, Translators.POS)
        connector_pos = PosConnector()
        allocator_ltc = LtcAllocator()
        translator_ltc_json = Translator(Translators.LTC, Translators.JSON)
        saver_ltc = ResourceSaver(ResourceManager.LTC, Files.RAW)

        starter.to(saver_ltc)
        srt_provider.to(purifier_srt, purifier_parse)

        purifier_parse.to(allocator_ltc)

        purifier_srt.to(preparer_srt).to(fetcher).to(translator_json_pos) \
            .to(connector_pos).to(allocator_ltc).to(translator_ltc_json).to(saver_ltc).to(finisher)

    def load_ltc(self, starter, finisher, last):
        starter.to(ResourceLoader(ResourceManager.LTC)).to(finisher)


def main(id, e, s):
    plain = f"id={id}&e={e}&s={s}"

    req = Request.of(plain)

    log_process("\n\n" + "-" * 30 + f"\n\n {req} is started the process")

    sublem = SubtitleLemmatizer()
    sublem.lemmatize(req)


id = "0898266"
id2 = "5753856"
succes = 0
for i in range(1, 18):
    for j in range(1, 5):
        try:
            main(id, i, j)
            succes += 1
        except Exception as e:
            print(e)
print("SUCCESS:", succes)
#main(id, 7, 3)
#for i in range(1, 4):
#main(id, 13, 1)
