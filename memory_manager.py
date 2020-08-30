import os, time


def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total

directories = ["./resources/ltc", "./resources/srt"]

def clear_directory(dir, hours):
    for f in os.listdir(dir):
        full = os.path.join(dir, f)
        if os.stat(full).st_mtime < time.time() - hours*60*60:
            print("Clearing", str(f), os.stat(full).st_mtime, "older than", hours*60*60, "seconds")
            os.remove(full)


def remove_old_if_no_memory(hours, megabytes):
    mbs = get_directory_size(".") / 1000000
    print("Project size", mbs)
    if mbs > megabytes:
        for dir in directories:
            clear_directory(dir, hours)

#if __name__ == '__main__':
    #remove_old_if_no_memory(0.5, 9)
