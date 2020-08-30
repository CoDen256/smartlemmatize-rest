from core.data.timecode import LemmatizedTimeCode
from core.utils import log_process
import re


class Allocator:

    def __init__(self):
        self.subtitles = None
        self.lemmata = None
        self.last_index = -1

    def allocate(self, subtitles, lemmata):
        log_process("Allocating...")
        self.subtitles = subtitles
        self.lemmata = lemmata
        return self.process()

    def get_subtitle(self, index, current):
        start, end, sub = self.parse(index)

        if self.last_index == index:
            return start, end, current

        self.last_index = index
        return start, end, sub

    def parse(self, index):
        line = self.subtitles[index]
        return Allocator.format_time(line.start), Allocator.format_time(line.end), line.content

    def get_lemmata(self, index):
        return self.lemmata[index]

    @staticmethod
    def format_time(time):
        return str(time)

    def process(self):
        result = []
        lemmata_per_time_code = []

        lemma_index = 0
        subtitle_index = 0

        start, end, subtitle = self.get_subtitle(subtitle_index, None)

        while True:
            if lemma_index >= len(self.lemmata) or subtitle_index >= len(self.subtitles): break

            lemma = self.get_lemmata(lemma_index)
            start, end, subtitle = self.get_subtitle(subtitle_index, subtitle)

            if not subtitle:
                result.append(LemmatizedTimeCode(lemmata_per_time_code, start, end))

                subtitle_index += 1
                lemmata_per_time_code = []
                continue

            matches = list(re.finditer(lemma.original, subtitle, flags=re.IGNORECASE))
            if matches:
                match = matches[0]
                lemmata_per_time_code.append(lemma)
                subtitle = self.remove_lemma(subtitle, match)
                lemma_index += 1
            else:
                subtitle = ""

        return result

    @staticmethod
    def trim_to_word(line):
        for i, char in enumerate(line):
            if char.isalpha():
                return line[i:]
        return ""

    @staticmethod
    def remove_lemma(line, index):
        return line[index.end(0):]
