class Files:
    BYTE, RAW, PRETTY = 1, 2, 4
    DEFAULT_ENCODING = "utf-8-sig"


class Translators:
    JSON, LTC, POS = 1, 2, 4


class PureCodes:
    CARRIAGE = 1 << 0
    TIME_CODES = 1 << 1
    ADS = 1 << 2
    REMARKS = 1 << 3
    TRIPLE_DOTS = 1 << 4
    TAGS = 1 << 5
    NAMES = 1 << 6
    DIALOG = 1 << 7
    NEW_LINES = 1 << 8
    SPLIT = 1 << 9
    STRIP = 1 << 10

    ALL = CARRIAGE | TIME_CODES | ADS | REMARKS | TRIPLE_DOTS | TAGS | NAMES | DIALOG | NEW_LINES | SPLIT | STRIP
