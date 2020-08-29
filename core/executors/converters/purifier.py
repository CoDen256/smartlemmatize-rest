from core.data.enums import PureCodes, Constants
import re
import srt


class Purifier:

    def __init__(self, stages=None):
        self.stages = PureCodes.ALL if stages is None else stages
        self.result = None

    def apply(self, to_purify):
        self.result = to_purify

        self.check_and_execute(PureCodes.ADS, self.remove_ad)
        self.check_and_execute(PureCodes.TAGS, self.remove_tags)
        self.check_and_execute(PureCodes.NAMES, self.remove_speaking_names)
        self.check_and_execute(PureCodes.REMARKS, self.remove_script_remarks)
        self.check_and_execute(PureCodes.TRIPLE_DOTS, self.remove_triple_dots)
        self.check_and_execute(PureCodes.DIALOG, self.remove_dialog_markers)
        self.check_and_execute(PureCodes.ABBREVIATIONS, self.remove_abbreviations)
        self.check_and_execute(PureCodes.PARSE, self.parse)

        self.check_and_execute(PureCodes.SPLIT, self.split_by_sentences)

        return self.result

    def check_and_execute(self, bit, callback):
        if self.stages & bit:
            self.result = callback(self.result)

    @staticmethod
    def remove_ad(res):
        reg = r"(Hier könnte deine Werbung stehen!\s|Kontaktiere noch heute www\.OpenSubtitles\.org\s)"
        res = re.sub(reg, "", res)

        reg2 = r"\[German - SDH\]"
        res = re.sub(reg2, "", res, flags=re.DOTALL)

        return res

    @staticmethod
    def remove_script_remarks(res):
        replace = lambda r: (r.lower()[1:-1] + ".")

        res = re.sub(r'\((.*[\n]?.*)\)', lambda r: replace(r.group(0)), res)

        return res

    @staticmethod
    def remove_triple_dots(res):  # sometimes ends with .? or something like this
        res = re.sub(r'\.\.\.', ".", res)
        res = re.sub(r'\.\?', '?', res)

        return res

    @staticmethod
    def remove_tags(res):
        # <i> sometimes doesn't have a dot. thus the line will go with next line as one sentence
        return re.sub(r"</?i>", "", res)

    @staticmethod
    def remove_speaking_names(res):
        return re.sub(r"[A-Z]+:\s?", "", res)

    @staticmethod
    def remove_dialog_markers(res):
        return re.sub(r"-([\s\w])", r" \1", res)

    @staticmethod
    def remove_abbreviations(res):
        return re.sub(Constants.DOT_REGEX, lambda o: re.sub(r"\.", "", o.group(0)), res, flags=re.IGNORECASE)

    @staticmethod
    def parse(res):
        return list(srt.parse(res))

    @staticmethod
    def split_by_sentences(res):
        temp = [""]
        for line in res:
            content = line.content
            content = re.split(r"[.?!]", content)

            for i, sent in enumerate(content):
                sent = sent.strip()
                last = temp[-1]
                endln = "" if i == len(content) - 1 else '.'

                if last.endswith("."):
                    temp.append(Purifier.last_formatting(sent) + endln)
                else:
                    temp[-1] = Purifier.last_formatting(last + " " + sent + endln)
        return temp

    @staticmethod
    def last_formatting(res):
        res = res.strip()
        res = re.sub("\"", "", res)
        res = re.sub(r"[\n:]", " ", res)
        return res

    def optimize_ads_tags_names_removal(self):
        reg = r"(Hier könnte deine Werbung stehen!\s|Kontaktiere noch heute www\.OpenSubtitles\.org\s|"\
                r"\[German - SDH\]|</?i>|[A-Z]+:\s?)"
        self.result = re.sub(reg, "", self.result)
