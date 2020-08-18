from data.query import Query

from handlers.lemma_connector import LemmaConnector
from handlers.lemma_fetcher import LemmaFetcher
from handlers.subtitle_fetcher import SubtitleFetcher
from handlers.subtitle_purifier import SubtitlePurifier
from handlers.reader import Reader
from handlers.writer import Writer
from handlers.time_stamper import TimeStamper
from handlers.json_translator import JSONTranslator

from handlers.parents.srt_provider import SRTProvider
from handlers.parents.ltc_provider import LTCProvider

from handlers.resource_manager import ResourceManager

class SubtitleLemmatizer:
    # imdb_id - id of movie on imdb.  https://www.imdb.com/  => search => url ../title/tt{ID}/...
    # season - season of movie
    # episode - episode of movie
    def lemmatize(self, query):    # return JSON(List[LemmatizedTimeCode])
        if (not isinstance(query, Query)): raise Exception("Parameters were not fully specified")

        manager = ResourceManager()

        srt_root1 = Reader()
        srt_root2 = SubtitleFetcher()

        ltc_root1 = Reader()
        ltc_root2 = SubtitlePurifier()

        ltc_root2.link(LemmaFetcher()).link(LemmaConnector()).link(TimeStamper()).link(JSONTranslator())

        srt = SRTProvider(manager,
                          srt_root1,
                          srt_root2)

        ltc = LTCProvider(manager,
                          ltc_root1,
                          ltc_root2)

        ltc.link(srt)

        ltc.handle(query)
        return None;

def main(id, e, s):
    plain = f"id={id}&e={e}&s={s}"

    query = Query.of(plain)

    sublem = SubtitleLemmatizer()
    result = sublem.lemmatize(query)

    print("SubLem:",result)


main("0898266",1,1)