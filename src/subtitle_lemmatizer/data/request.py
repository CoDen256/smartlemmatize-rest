class Request:
    def __init__(self, id, season, episode):
        self.id = id
        self.season = season
        self.episode = episode

        self._content = None


    @staticmethod
    def toDict(plain):
        q = plain.split("&")
        result = {}
        for param in q:
            key, value = tuple(param.split("="))
            result[key] = value

        return result

    @staticmethod
    def of(plain):
        try:
            d = Query.toDict(plain)
            return Query(id=d["id"], 
                         season=d["s"], 
                         episode=d["e"])
        except:
            raise Exception("Illegal arguments")

    def getContent(self):
        return self._content

    def setContent(self, content):
        self._content = content

    def __str__(self):
        return f"Query({self.id}, {self.season}, {self.episode})"