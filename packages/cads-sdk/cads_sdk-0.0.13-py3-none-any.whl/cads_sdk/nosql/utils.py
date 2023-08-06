import spark_sdk as ss
import os

def check_delta(input_path):
    list_file = ss.ls(input_path)
    for f in list_file:
        if '_delta_log' in f:
            return True
    return False

def get_size_of_dir(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_size_of_dir(entry.path)
    return total


def get_size_of_list(input_files):
    total = sum([os.stat(path).st_size for path in input_files])
    return total