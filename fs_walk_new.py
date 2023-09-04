import os
import sys
from typing import Tuple
import unicodedata
import keyboard as kb

def _is_folder(path: str):
    """ Wrapper function for os.path.isdir() """
    if os.path.isdir(path):
        return True
    return False

FS_CACHE = []
SEARCH_CACHE = []

def filter_fs(item: Tuple[str, int], file_type: str=None, item_type: str=None): # item_type "dir", "file" or "all"
    """ Applies the given filter to each step and yields the result. """
    if file_type is None:
        if item_type is None or item_type == "all":
            SEARCH_CACHE.append(item)
            yield item
        elif item_type == "dir":
            if item[1] == "dir":
                SEARCH_CACHE.append(item)
                yield item
        elif item_type == "file":
            if item[1] == "file":
                SEARCH_CACHE.append(item)
                yield item
    if item[0].endswith(file_type):
        SEARCH_CACHE.append(item)
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
    at each step. Also keeps track of the current directory. Yields the 
    result and it's current directory. """
    current_dir = None
    for (i, step) in enumerate(fswalk("C:\\")):
        if step[1] == "dir":
            current_dir = step[0]
            #print(current_folder)
        for item in filter_fs(step, filter):
            yield (item, os.path.dirname(os.path.realpath(current_dir)))
        
#//////////// TUI /// 
finished = False
search_filters = []
while not finished:
    search_filters.append(input("Search: "))
    if search_filters[0] == "-q":
        break
    if search_filters[-1] == "-q":
        search_filters.pop(-1)
        print("SEARCHING FOR %s" % search_filters)
        for i in range(len(search_filters)):
            for (count, step) in enumerate(start_fswalk(search_filters[i])):
                print(count, step[0][0], step[1]) # do something with step here???
                print(FS_CACHE)
                finished = True
                break
