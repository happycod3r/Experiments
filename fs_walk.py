import os
from typing import Tuple
import unicodedata
import keyboard as kb
from datetime import datetime as dt

FS_CACHE = []
SEARCH_CACHE = []

def _cache():
    with open("cache.txt", "w") as file:
        for i in range(len(SEARCH_CACHE)):
            file.write(SEARCH_CACHE[i]) 
        file.close()

def _check_fs_cache(query: str):
    for i in range(len(FS_CACHE)):
        for j in range(len(FS_CACHE[i])):
            if query in FS_CACHE[i][j]:
                return FS_CACHE[i]
    return None

def _check_search_cache(query: str):
    for i in range(len(SEARCH_CACHE)):
        if query in SEARCH_CACHE[i]:
            return SEARCH_CACHE[i]
    return None

def _is_folder(path: str):
    """ Wrapper function for os.path.isdir() """
    if os.path.isdir(path):
        return True
    return False

def filter_fs(item: Tuple[str, int], file_type: str=None, item_type: str=None): # item_type "dir", "file" or "all"
    """ Applies the given filter to each step and yields the relative results. """
    if file_type is None:
        if item_type is None or item_type == "all":
            yield item
        elif item_type == "dir":
            if item[1] == "dir":
                yield item
        elif item_type == "file":
            if item[1] == "file":
                yield item
    if item[0].endswith(file_type):
        yield item
 
def fswalk(path: str):
    """ Steps through the file system starting at the root C:\\ directory 
    and labels each step as either a file or directory. """
    try:
        for step in os.walk(f"{path}"):
            for item in step:
                if isinstance(item, list):
                    for i in range(len(item)):
                        if _is_folder(item[i]):
                            yield (item[i], "dir") # DIR
                            continue
                        yield (item[i], "file") # FILE
                    continue
                if _is_folder(item):
                    yield (item, "dir") # DIR
                    continue
                yield (item, "file") # FILE
    except UnicodeEncodeError as e:
        print(f"Couldn't process unicode character!\n{e}")    

def start_fswalk(filter):
    """ Begins the walk through the file system and applies the given filter
    at each step. Also keeps track of the current directory, caches each step
    on the walk and yields the relevant results and it's current directory. """
    current_dir = None
    for (i, step) in enumerate(fswalk("C:\\")):
        if step[1] == "dir":
            current_dir = step[0]
        for item in filter_fs(step, filter):
            result_path = os.path.dirname(os.path.realpath(current_dir))
            yield (item, result_path)
 
def timer(start, end):
    _starttime = start.split(':')
    _starttime = [int(timeseg) for timeseg in _starttime]
    _endtime = end.split(':')
    _endtime = [int(timeseg) for timeseg in _endtime]
    time_taken = ''
    for i in range(2):
        diff = _endtime[i] - _starttime[i]
        time_taken += str(diff) + ":"
    return time_taken

def init_tui():
#//////////// TUI //////
    finished = False
    search_filters = []
    while not finished:
        search_filters.append(input("Search: "))
        if search_filters[0] == "-q":
            break
        if search_filters[-1] == "-q":
            search_filters.pop(-1)
            print("SEARCHING FOR %s" % search_filters)
            starttime = dt.now().strftime("%M:%S")
            for i in range(len(search_filters)):
                for (count, step) in enumerate(start_fswalk(search_filters[i])):
                    print(count, step[0][0], step[1])
                    # Break out of the program if there are no more search
                    # filters to process.
                    # Removing finished = True or never assigning it a True value
                    # will start a new search after finishing the current search_filters 
                    endtime = dt.now().strftime("%M:%S")
                    print(starttime, endtime)
                    finished = True  
                    break

init_tui()

# Flag988.flag C:\Users\paulm
# t1 - 14:17 14:42 - 25s
# t2 - 16:19 16:42 - 23s
# t3 - 21:36 21:59 - 23s
# t4 - 24:18 24:41 - 23s

# Flag987.flag C:\Users\paulm
# t1 - 14:17 15:08 - 51s
# t2 - 16:19 17:05 - 46s
# t3 - 21:36 22:22 - 46s
# t4 - 24:18 25:04 - 46s

