from core.data.enums import Constants


class CabWebService:
    API = "http://www.deutschestextarchiv.de/demo/cab/query?a=caberr&fmt=json&clean=1&q={query}"
    DEVIATION = 1  # can happen because of new lines 1-2 symbols

    @staticmethod
    def fetch(sentences):
        from core.executors.web_services.fetcher import Fetcher
        if any([len(s) > Constants.MAX_LENGTH + CabWebService.DEVIATION for s in sentences]):
            raise Exception("Length of sentence is exceeded, url will not be fethced, abort")

        if isinstance(sentences, str):
            raise Exception("Sentences is string, abort")

        responses = Fetcher.fetch(*[CabWebService.API.format(query=s) for s in sentences])

        if any([r is None or not r.ok for r in responses]):
            raise Exception("Chunks was not fetched successfully, abort")

        return [r.json() for r in responses]

    @staticmethod
    def fetchOne(query):
        from core.executors.web_services.fetcher import Fetcher

        response = Fetcher.fetchOne(CabWebService.API.format(query=query))

        if response is None or not response.ok:
            raise Exception("Query was not fetched successfully, abort")

        return response.json()
