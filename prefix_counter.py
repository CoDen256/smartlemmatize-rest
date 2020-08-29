import os
import re

dir = "./resources/ltc"


for f in os.listdir(dir):
    inhalt = open(dir+"/"+f, "r", encoding="utf-8-sig")
    result = re.findall(r"\"prefix\": \"\w", inhalt.read())
    print(f, len(result))


