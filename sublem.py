from core.data import Request
from core.handlers import *
from core.providers import *
from core.handlers.subtitle_purifier import ALL
from core.executors import CabWebService
from core.resource_manager import ResourceManager
from core.files.writer import JSON, BYTE
from core.utils import assertType, log, logProcess


class SubtitleLemmatizer:
    # imdb_id - id of movie on imdb.  https://www.imdb.com/  => search => url ../title/tt{ID}/...
    # season - season of movie
    # episode - episode of movie

    def lemmatize(self, query):  # return JSON(List[LemmatizedTimeCode])
        assertType("query", query, Request)

        manager = ResourceManager()

        srt_loader = ResourceLoader(manager.SRT)
        srt_branch = SubtitleFetcher()
        srt_branch.link(Unzipper()).link(ResourceSaver(manager.SRT, BYTE))

        srt = SRTProvider(manager, srt_loader, srt_branch)

        ltc_loader = ResourceLoader(manager.LTC)
        ltc_branch = SubtitlePurifier(ALL)
        ltc_branch.link(Splitter(CabWebService.MAX_LENGTH, decapitalize=True)) \
            .link(LemmaFetcher()) \
            .link(JSONTranslator(Content.JSON, Content.POS)) \
            .link(LemmaConnector()) \
            .link(TimeStamper(srt)) \
            .link(JSONTranslator(Content.LTC, Content.JSON)) \
            .link(ResourceSaver(manager.LTC, JSON))

        ltc = LTCProvider(manager, ltc_loader, ltc_branch)

        ltc.link(srt)
        r = ltc.handle(query)
        logProcess("\nCHAIN: ", r.chain)
        return r.getContent()


def main(id, e, s):
    plain = f"id={id}&e={e}&s={s}"

    req = Request.of(plain)

    logProcess("\n\n" + "-" * 30 + f"\n\n {req} is started the process")

    sublem = SubtitleLemmatizer()
    result = sublem.lemmatize(req)

    log("sublem.json", result, JSON)


main("0898266", 1, 1)
