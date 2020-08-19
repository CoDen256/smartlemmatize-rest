from core.data import Request

from core.handlers import *

from core.providers import *

from core.resource_manager import ResourceManager
from core.utils import assertType

class SubtitleLemmatizer:
    # imdb_id - id of movie on imdb.  https://www.imdb.com/  => search => url ../title/tt{ID}/...
    # season - season of movie
    # episode - episode of movie
    def lemmatize(self, query):    # return JSON(List[LemmatizedTimeCode])
        assertType("query", query, Request)

        manager = ResourceManager()

        srt_loader = Loader(manager.SRT)
        srt_branch = SubtitleFetcher()

        ltc_loader = Loader(manager.LTC)
        ltc_branch = SubtitlePurifier()

        ltc_branch.link(LemmaFetcher()).link(LemmaConnector()).link(TimeStamper()).link(JSONTranslator())

        srt = SRTProvider(manager,
                          srt_loader,
                          srt_branch)

        ltc = LTCProvider(manager,
                          ltc_loader,
                          ltc_branch)

        ltc.link(srt)
        r = ltc.handle(query)
        print("REMARKS", r.chain)
        return r.getContent()

def main(id, e, s):
    plain = f"id={id}&e={e}&s={s}"

    query = Request.of(plain)

    sublem = SubtitleLemmatizer()
    result = sublem.lemmatize(query)

    #print("SubLem:",result)


main("0898266",1,1)