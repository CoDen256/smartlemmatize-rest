class Query:
    def __init__(self, id, season, episode):
        self.id = id
        self.season = season
        self.episode = episode

    def toDict(plain):
        q = plain.split("&")
        result = {}
        for param in q:
            key, value = tuple(param.split("="))
            result[key] = value

        return result

    def of(plain):
        try:
            d = Query.toDict(plain)
            return Query(id=d["id"], 
                         season=d["s"], 
                         episode=d["e"])
        except:
            raise Exception("Illegal arguments")
