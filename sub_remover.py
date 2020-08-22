import os

directories = ["./resources/ltc", "./resources/srt"]

def clear_directory(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

for dir in directories:
    clear_directory(dir)
