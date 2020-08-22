from core.services.fetcher import Fetcher

class CabWebService:
    API = "http://www.deutschestextarchiv.de/demo/cab/query?a=caberr&fmt=json&clean=1&q={query}"
    MAX_LENGTH = 1745 

    @staticmethod
    def fetch(sentences):
        if any([len(s) > CabWebService.MAX_LENGTH for s in sentences]):
            raise Exception("Length of sentence is exceeded, url will not be fethced, abort")
        
        responses = Fetcher.fetch([API.format(s) for s in sentences])

        if any([not r.ok for r in responses]):
            raise Exception("One chunk was not fetched successfully, abort")
        
        return [r.json() for r in responses]