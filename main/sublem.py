from data.query import Query


from handlers.lemma_connector import LemmaConnector
from handlers.lemma_fetcher import LemmaFetcher
from handlers.subtitle_fetcher import SubtitleFetcher
from handlers.subtitle_porifier import SubtitlePurifier
from handlers.reader import Reader
from handlers.writer import Writer
from handlers.time_stamper import TimeStamper

class SubtitleLemmatizer:
    # imdb_id - id of movie on imdb.  https://www.imdb.com/  => search => url ../title/tt{ID}/...
    # season - season of movie
    # episode - episode of movie
    def lemmatize(self, query):    # return JSON(List[LemmatizedTimeCode])
        if (not isinstance(query, Query)): raise Exception("Parameters were not fully specified")

        handler = Reader().set_child(TimeStamper())\
                          .set_child(LemmaConnector())\
                          .set_child(LemmaFetcher())\
                          .set_child(SubtitlePurifier())\
                          .set_child(SubtitleFetcher())

        return None;

def main(id, e, s):
    plain = "id={id}&e={e}&s={s}"

    query = Query.of(plain)

    sublem = SubtitleLemmatizer()
    result = sublem.lemmatize(query)

    print("SubLem:",result)


main("0898266",1,1)