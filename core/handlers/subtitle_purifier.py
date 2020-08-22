from core.handlers.handler import AbstractHandler
from core.files.writer import Writer
import re

TIME_CODES = 1 << 0
ADS = 1 << 1
REMARKS = 1 << 2
TRIPLE_DOTS = 1 << 3
TAGS = 1 << 4
NAMES = 1 << 5
DIALOG = 1 << 6
NEW_LINES = 1 << 7
SPLIT = 1 << 8
STRIP = 1 << 9

ALL = TIME_CODES | \
      ADS | \
      REMARKS | \
      TRIPLE_DOTS | \
      TAGS | \
      NAMES | \
      DIALOG | \
      NEW_LINES | \
      SPLIT | \
      STRIP 

#TODO HANDLERS AND EXECUTORS SEPARATE
class SubtitlePurifier(AbstractHandler):

    def __init__(self, stages=None):
        self.stages = ALL if stages == None else stages
        self.result = None

    def handle(self, request):
        self.purify(request.getContent())
        
        request.setContent(self.result)

        Writer.write_text("1_purifier.txt", self.result)

        return super().handle(request)

    def purify(self, toPurify):
        self.result = toPurify

        self.checkExecute(TIME_CODES, self.removeTimeCodes)
        self.checkExecute(ADS, self.removeAd)
        self.checkExecute(REMARKS, self.removeScriptRemarks)
        self.checkExecute(TRIPLE_DOTS, self.removeTripleDots)
        self.checkExecute(TAGS, self.removeTags)
        self.checkExecute(NAMES, self.removeSpeakingNames)
        self.checkExecute(DIALOG, self.removeDialogMarkers)
        self.checkExecute(NEW_LINES, self.removeNewLines)
        self.checkExecute(SPLIT, self.newLinePerSentence)
        self.checkExecute(STRIP, self.stripLines)
    
    def checkExecute(self, bit, callback):
        if self.stages & bit: callback()

    def removeTimeCodes(self):
        res = self.result

        reg = r"\d+[\n]\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}[\n]"
        res =  re.sub(reg, "", res)

        self.result = res

    def removeAd(self):
        res = self.result

        reg = "\nHier könnte deine Werbung stehen!\nKontaktiere noch heute www.OpenSubtitles.org\n"
        res = re.sub(reg, "", res)

        reg2 = r".\[German - SDH\].*OpenSubtitles.*"
        res = re.sub(reg2, "", res, flags=re.DOTALL)

        self.result = res

    def removeScriptRemarks(self):
        res = self.result
        
        replace = lambda r: (r.lower()[1:-1]+".").title()

        res = re.sub(r'\((.*[\n]?.*)\)', lambda r: replace(r.group(0)), res) 

        self.result = res

    def removeTripleDots(self): # sometimes ends with .? or something like this
        res = self.result

        res = re.sub(r'\.\.\.', ".", res)
        res = re.sub(r'\.\?', '?', res)

        self.result = res

    def removeTags(self): # <i> sometimes doesn't have a dot. thus the line will go with next line as one sentence
        res = self.result

        res = re.sub(r"<\/?i>", "", res)

        self.result = res

    def removeSpeakingNames(self):
        res = self.result

        res = re.sub(r"[A-Z]{2,}:[\s\n]", "", res)

        self.result = res

    def removeDialogMarkers(self):
        res = self.result

        res = re.sub(r"^- ", "", res, flags=re.MULTILINE)

        self.result = res

    def removeNewLines(self):
        res = self.result

        res = re.sub(r"[\n]", " ", res)

        self.result = res

    def newLinePerSentence(self): # can cause artifacts by Z.B, "etc." and other short forms
        res = self.result

        replace = lambda r: r+"\n"

        res = re.sub(r'([\.\?\!]\"?)', lambda r: replace(r.group(0)), res) 

        self.result = res

    def stripLines(self):
        res = self.result

        replace = lambda r: r.strip() + "\n"

        res = re.sub(r'(^[^\n]*\n)', lambda r: replace(r.group(0)), res, flags=re.MULTILINE) 

        self.result = res

    def getResult(self):
        return self.result