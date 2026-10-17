from pathlib import Path

def load_notes(folder="notes"):
    notes = []
    for file in Path(folder).glob("*.txt"):
        notes.append({"name": file.name, "text": file.read_text(encoding="utf-8")})
    return notes

def chunk_notes(notes):
    chunks = []
    for note in notes:
        for line in note["text"].splitlines():
            line = line.strip()
            if line:
                chunks.append({"source": note["name"], "text": line})
    return chunks

if __name__ == "__main__":
    notes = load_notes()
    chunks = chunk_notes(notes)
    print(len(chunks), "chunks")
    print(chunks[0])