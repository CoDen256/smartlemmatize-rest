import os
import re

direc = "./resources/ltc"

for f in os.listdir(direc):
    try:
        inhalt = open(direc+"/"+f, "r", encoding="utf-8")
        result = re.findall(r"\"prefix\": \"\w", inhalt.read())
        print(f, len(result))
    except:
        print(f, "UNABLE TO OPEN")


