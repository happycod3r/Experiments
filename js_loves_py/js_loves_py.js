const fs = require('fs')

function sendNoteToPy(note, file_path) {
    try {
        fs.writeFileSync(file_path, JSON.stringify(note))
    }
    catch (err) {
        console.info(err.message)
    }
}

function getNoteFromPy(filePath) {
    try {
        note_from_py = JSON.parse(fs.readFileSync(filePath))
        return note_from_py
    }
    catch(err) {
        console.info(err.message)
    }
}

note = {
    "name": "javascript",
    "text": "Hello Python!"
}
sendNoteToPy(note, "note_from_js.json")
#console.info(getNoteFromPy("note_from_py.json"))
