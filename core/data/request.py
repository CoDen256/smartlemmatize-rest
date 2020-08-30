from core.data.encodings import getEncoding, setEncoding

class Request:
    def __init__(self, id, season, episode):
        self.id = id
        self.season = season
        self.episode = episode

        self.encoding = getEncoding(id, season, episode)

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
            d = Request.toDict(plain)
            return Request(id=d["id"],
                           season=d["s"],
                           episode=d["e"])
        except Exception as e:
            raise Exception("Illegal arguments")

    def setEncoding(self, encoding):
        self.encoding = setEncoding(self.id, self.season, self.episode, encoding=encoding)


    def __str__(self):
        return f"Request({self.id}, {self.season}, {self.episode})"

    def __repr__(self):
        return self.__str__()
