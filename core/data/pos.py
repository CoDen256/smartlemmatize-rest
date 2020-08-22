class PartOfSpeech:
    def __init__(self, original, main, wordType):
        self.original = original
        self.main = main
        self.wordType = wordType

        self.args = {}

    def __str__(self):
         return  str({
            "orig" : self.original,
            "main" : self.main,
            "type" : self.wordType,
            "args" : self.args # reflex = true/false, prefix
            })

    def __repr__(self):
        return self.__str__()
