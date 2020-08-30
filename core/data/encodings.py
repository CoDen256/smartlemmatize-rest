import os

ENCODINGS_PATH = os.path.abspath("./resources/encodings.cfg")

def getEncoding(id, season, episode):
    with open(ENCODINGS_PATH, "r", encoding="utf-8", ) as f:
        encodings = f.readlines()
        for line in encodings:
            unique, enc = line.split("=")
            if unique == f"{id}_{season}_{episode}":
                return enc
        return None


def setEncoding(id, season, episode, encoding):
    existing = getEncoding(id, season, episode)
    if existing is None:
        with open(ENCODINGS_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{id}_{season}_{episode}={encoding}")
        return encoding
    return existing
