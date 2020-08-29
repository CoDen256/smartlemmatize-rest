class LemmatizedTimeCode:
    def __init__(self, lemmas, start, end):
        self.lemmas = lemmas  # Lemmas of all the words in this period
        self.start = start  # Start of the timecode, to which this lemmas refer
        self.end = end  # End of the timecode, to which this lemmas refer

    def __str__(self):
        return str({
            "lemmas": str(self.lemmas),
            "start": self.start,
            "end": self.end,
        })

    def __repr__(self):
        return self.__str__()
