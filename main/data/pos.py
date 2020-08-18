class PartOfSpeech:
    def __init__(self, original, main, wordType):
        self.original = original
        self.main = main
        self.wordType = wordType

        self.args = {}