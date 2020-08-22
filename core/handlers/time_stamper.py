from core.handlers.handler import AbstractHandler
from core.handlers.subtitle_purifier import ALL, TIME_CODES, NEW_LINES, SPLIT, STRIP, SubtitlePurifier
from core.data.timecode import LemmatizedTimeCode
from core.files.writer import Writer
import re

class TimeStamper(AbstractHandler):
    def __init__(self, srtProvider):
        self.srtProvider = srtProvider;
    
    def handle(self, request): #TODO maybe link another handler, so method will be called 2 times, and will be executed accordingly
        #TODO each handle has to be checked by type
        #TODO time measurement
        lemmata = request.getContent()
        raw = self.srtProvider.handle(request).getContent()

        result = self.stamp(self.purify(raw), lemmata)
        request.setContent(result)

        Writer.write_iter("5_time_stamper.txt", result)

        return super().handle(request)

    def splitByTime(self, raw):
        return raw.split("\n\n")

    def parseLine(self, line):
        _, interval, *text = line.split("\n")
        start, end = interval.split(" --> ")

        text = " ".join(text)
        return start, end, text

    def process(self, splited, lemmas):
        result = []

        currentLemma = 0
        currentOriginal = 0

        start, end, currentOriginalLine = self.parseLine(splited[currentOriginal])
        lemmata =  []
        while True:
            lemma = lemmas[currentLemma]

            if lemma.original.lower() in currentOriginalLine.lower():
                lemmata.append(lemma)
                try:
                    currentOriginalLine = re.sub(re.escape(lemma.original), "", currentOriginalLine, flags=re.IGNORECASE,count=1)
                except Exception as e:
                    print("UNABLE TO PROCCESS LINE:", currentOriginalLine, "<->",  lemma.original, e)

                currentLemma += 1
                if (currentLemma >= len(lemmas)): break

            else:
                result.append(LemmatizedTimeCode(lemmata, start, end))
                currentOriginal += 1
                if (currentOriginal >= len(splited)): break
                lemmata = []
                start, end, currentOriginalLine = self.parseLine(splited[currentOriginal])


        return result

    def purify(self, raw):
        purifier = SubtitlePurifier(ALL ^ TIME_CODES ^ NEW_LINES ^ SPLIT ^ STRIP)
        purifier.purify(raw)
        return purifier.result

    def stamp(self, pure, lemmata):
        return self.process(self.splitByTime(pure), lemmata)