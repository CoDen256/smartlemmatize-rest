class Query:
    def __init__(self, id, season, episode):
        self._id = id
        self._season = season
        self._episode = episode
        self.remarks = "" #! remove

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

        
    def __str__(self):
        return f"Query({self._id}, {self._season}, {self._episode})"