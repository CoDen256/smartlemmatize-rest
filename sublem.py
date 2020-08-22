from core.data import Request

from core.handlers import *

from core.providers import *

from core.handlers.subtitle_purifier import ALL

from core.files import Writer

from core.services.cab_web_service import CabWebService

from core.resource_manager import ResourceManager
from core.utils import assertType

class SubtitleLemmatizer:
    # imdb_id - id of movie on imdb.  https://www.imdb.com/  => search => url ../title/tt{ID}/...
    # season - season of movie
    # episode - episode of movie
    def lemmatize(self, query):    # return JSON(List[LemmatizedTimeCode])
        assertType("query", query, Request)

        manager = ResourceManager()

        srt_loader = ResourceLoader(manager.SRT)
        srt_branch = SubtitleFetcher()

        srt = SRTProvider(manager,
                          srt_loader,
                          srt_branch)

        ltc_loader = ResourceLoader(manager.LTC)

        ltc_branch = SubtitlePurifier(ALL)
        ltc_branch.link(Splitter(CabWebService.MAX_LENGTH, decapitalize=True))\
        .link(LemmaFetcher())\
        .link(JSONTranslator(Content.JSON, Content.POS))\
        .link(LemmaConnector())\
        .link(TimeStamper(srt))\
        .link(JSONTranslator(Content.LTC, Content.JSON))\
        .link(ResourceSaver(manager.LTC))

        ltc = LTCProvider(manager,
                          ltc_loader,
                          ltc_branch)

        ltc.link(srt)
        r = ltc.handle(query)
        print("\nCHAIN: ", r.chain)
        return r.getContent()

def main(id, e, s):
    plain = f"id={id}&e={e}&s={s}"

    query = Request.of(plain)

    sublem = SubtitleLemmatizer()
    result = sublem.lemmatize(query)

    Writer.write("result.txt", result)


main("0898266",1,1)