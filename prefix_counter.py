import os
import re

direc = "./resources/ltc"

for f in os.listdir(direc):
    inhalt = open(direc+"/"+f, "r", encoding="utf-8-sig")
    result = re.findall(r"\"prefix\": \"\w", inhalt.read())
    print(f, len(result))


