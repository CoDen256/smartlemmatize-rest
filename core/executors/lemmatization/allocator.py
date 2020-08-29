from core.data.timecode import LemmatizedTimeCode
import re
from difflib import SequenceMatcher


class Allocator:

    def allocate(self, subtitles, lemmata):
        return self.process(subtitles, lemmata)

    @staticmethod
    def parse_subtitle(line):
        return Allocator.format_time(line.start), Allocator.format_time(line.end), line.content

    @staticmethod
    def format_time(time):
        return str(time)
    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    def process(self, subtitles, lemmata):
        result = []

        current_lemma_count = 0
        current_line_count = 0

        start, end, current_original_line = self.parse_subtitle(subtitles[current_line_count])
        lemmata_per_time_code = []
        while True:
            lemma = lemmata[current_lemma_count]

            if lemma.original.lower() in current_original_line.lower():
                lemmata_per_time_code.append(lemma)

                current_original_line = self.trim_line(lemma, current_original_line)

                current_lemma_count += 1
                if current_lemma_count >= len(lemmata): break
            else:
                if not lemmata_per_time_code and self.parse_subtitle(subtitles[current_line_count])[-1] != current_original_line:
                    current_lemma_count += 1
                    if current_lemma_count >= len(lemmata): break
                    continue

                if self.parse_subtitle(subtitles[current_line_count])[-1] != current_original_line:
                    result.append(LemmatizedTimeCode(lemmata_per_time_code, start, end))

                current_line_count += 1
                if current_line_count >= len(subtitles): break
                lemmata_per_time_code = []
                start, end, current_original_line = self.parse_subtitle(subtitles[current_line_count])

        return result

    def trim_line(self, lemma, line):
        try:
            line = re.sub(re.escape(lemma.original), "", line,
                          flags=re.IGNORECASE, count=1)
            return line
        except Exception as e:
            print("UNABLE TO PROCCESS LINE:", line, "<->", lemma.original, e)
