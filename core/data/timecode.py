class LemmatizedTimeCode:
    def __init__(self, lemmas, start, end):
        self.lemmas = lemmas               # Lemmas of all the words in this period
        self.start = start                  # Start of the timecode, to which this lemmas refer
        self.end = end                      # End of the timecode, to which this lemmas refer