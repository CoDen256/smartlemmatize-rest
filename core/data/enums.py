import re
class Files:
    BYTE, RAW, PRETTY = 1, 2, 4
    DEFAULT_ENCODING = "utf-8-sig"


class Translators:
    JSON, LTC, POS = 1, 2, 4


class PureCodes:
    ADS = 1 << 1
    REMARKS = 1 << 2
    TRIPLE_DOTS = 1 << 3
    TAGS = 1 << 4
    NAMES = 1 << 5
    DIALOG = 1 << 6
    ABBREVIATIONS = 1 << 7
    PARSE = 1 << 8

    SPLIT = 1 << 9

    DEFAULT = ADS | REMARKS | TRIPLE_DOTS | TAGS | NAMES | DIALOG | ABBREVIATIONS
    ALL = DEFAULT | PARSE | SPLIT

    SPLIT_PARSED = PARSE | SPLIT


class Constants:
    ABBREVIATIONS = ["z.b.", "mr.", "ms.", "mrs.", "dr.", "etc."]
    DIGITS_REGEX = r"\d+\.\d+"
    DOT_REGEX = "(" + "|".join([re.escape(s) for s in ABBREVIATIONS]+[DIGITS_REGEX])+")"
