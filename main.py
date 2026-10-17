from pathlib import Path

def load_notes(folder="notes"):
    notes = []
    for file in Path(folder).glob("*.txt"):
        notes.append({"name": file.name, "text": file.read_text(encoding="utf-8")})
    return notes

if __name__ == "__main__":
    for note in load_notes():
        print(note["name"], "-", len(note["text"]), "characters")