import os
import sys
import unicodedata

def is_folder(path: str):
    if os.path.isdir(path): return True
    else: return False
    
def id_file(path: str):
    if os.path.isfile(path): return True
    else: return False
        
def step_through_path(path):
    try:
        for step in os.walk(f"{path}"):
            for item in step:
                if isinstance(item, list):
                    for i in range(len(item)):
                        if is_folder(item[i]):
                            print(f"DIR: {item[i]}")
                        else: print(f"FILE: {item[i]}")
                else:
                    if is_folder(item):
                        print(f"DIR: {item}")
                    else: print(f"FILE: {item}")
    except UnicodeEncodeError as e:
        print(f"Couldn't process unicode character!\n{e}")

step_through_path("C:\\")
