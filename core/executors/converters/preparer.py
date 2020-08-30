import re

class Preparer:
    def __init__(self, limit, decapitalize=False):
        self.decapitalize = decapitalize
        self.limit = limit
        if not self.limit or self.limit < 0: raise ValueError("Limit is not specified or incorrect")

    def split_and_prepare(self, sentences):
        if not sentences: raise Preparer.NothingToSplitException("Input is empty")

        temp = [""]
        for line in sentences:
            line = line.strip()
            line = re.sub(r"(\.)", r" \1 ", line)

            if len(line) <= 1: continue
            if len(line) > self.limit:
                raise Preparer.LineLengthExceededException(f"Limit: {self.limit}, Line: {line}")


            line = self.decapitalize_first_word(line)

            if len(temp[-1]) + len(line) > self.limit:
                temp.append(line)
            else:
                temp[-1] = temp[-1] + line

        return list(filter(lambda el: bool(el), temp))

    def decapitalize_first_word(self, sentence):
        if self.decapitalize:
            words = sentence.split(" ")
            words[0] = words[0].lower()
            sentence = " ".join(words)
        return sentence

    class LineLengthExceededException(Exception):
        pass

    class NothingToSplitException(Exception):
        pass

