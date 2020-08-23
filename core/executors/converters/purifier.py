from core.data.enums import PureCodes
import re


# .replace("\r", "")
# TODO RUN MULTIPLE REGEX .SUB, AT ONE TIME
class Purifier:

    def __init__(self, stages=None):
        self.stages = PureCodes.ALL if stages is None else stages
        self.result = None

    def purify(self, to_purify):
        self.result = to_purify

        self.check_and_execute(PureCodes.CARRIAGE, self.remove_carriage)
        self.check_and_execute(PureCodes.TIME_CODES, self.remove_time_codes)
        self.check_and_execute(PureCodes.ADS, self.remove_ad)
        self.check_and_execute(PureCodes.REMARKS, self.remove_script_remarks)
        self.check_and_execute(PureCodes.TRIPLE_DOTS, self.remove_triple_dots)
        self.check_and_execute(PureCodes.TAGS, self.remove_tags)
        self.check_and_execute(PureCodes.NAMES, self.remove_speaking_names)
        self.check_and_execute(PureCodes.DIALOG, self.remove_dialog_markers)
        self.check_and_execute(PureCodes.NEW_LINES, self.remove_new_lines)
        self.check_and_execute(PureCodes.SPLIT, self.new_line_per_sentence)
        self.check_and_execute(PureCodes.STRIP, self.strip_lines)

        return self.result

    def check_and_execute(self, bit, callback):
        if self.stages & bit:
            self.result = callback(self.result)

    @staticmethod
    def remove_carriage(res):
        return re.sub("\r", "", res)

    @staticmethod
    def remove_time_codes(res):
        regex = r"\d+[\n]\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}[\n]"
        return re.sub(regex, "", res)

    @staticmethod
    def remove_ad(res):
        reg = "\nHier könnte deine Werbung stehen!\nKontaktiere noch heute www.OpenSubtitles.org\n"
        res = re.sub(reg, "", res)

        reg2 = r".\[German - SDH\].*OpenSubtitles.*"
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
        return re.sub(r"[A-Z]{2,}:[\s\n]", "", res)

    @staticmethod
    def remove_dialog_markers(res):
        return re.sub(r"^- ", "", res, flags=re.MULTILINE)

    @staticmethod
    def remove_new_lines(res):
        return re.sub(r"[\n]", " ", res)

    @staticmethod
    def new_line_per_sentence(res):
        # can cause artifacts by Z.B, "etc." and other short forms
        replace = lambda r: r + "\n"
        return re.sub(r'([\.\?\!]\"?)', lambda r: replace(r.group(0)), res)

    @staticmethod
    def strip_lines(res):
        replace = lambda r: r.strip() + "\n"
        return re.sub(r'(^[^\n]*\n)', lambda r: replace(r.group(0)), res, flags=re.MULTILINE)
