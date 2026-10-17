from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

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

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    texts = [c["text"] for c in chunks]
    return model.encode(texts, normalize_embeddings=True)

def search(question, chunks, vectors, top_k=3):
    q = model.encode([question], normalize_embeddings=True)[0]
    scores = vectors @ q
    best = np.argsort(scores)[::-1][:top_k]
    return [(float(scores[i]), chunks[i]) for i in best]

if __name__ == "__main__":
    notes = load_notes()
    chunks = chunk_notes(notes)
    vectors = embed_chunks(chunks)
    print(vectors.shape)
    question = "How does a tap-to-pay card work without power of its own?"
    for score, chunk in search(question, chunks, vectors):
        print(round(score, 3), chunk["source"], "-", chunk["text"])