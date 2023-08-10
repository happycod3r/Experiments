import json

def send_note_to_js(note_data: dict, path: str):
    try:
        with open(path, 'x') as note:
            json.dump(note_data, note)
            note.close()
    except FileNotFoundError as e:
        print(repr(e))
    except IOError as e:
        print(repr(e))

def get_note_from_js(path: str):
    note_from_js = path
    try:
        with open(note_from_js, "r") as note:
            note_text = json.load(note)
            note.close()
            print(note_text)
    except FileNotFoundError as e:
        print(repr(e))
    except IOError as e:
        print(repr(e))

note = {
    "name": "Paul",
    "location": "22 33 78.12"
}

send_note_to_js(note, "note_from_py.json")
get_note_from_js("note_from_js.json")
