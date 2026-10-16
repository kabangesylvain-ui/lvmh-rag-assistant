"""
Ingestion des documents : chargement + chunking.
"""
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader

from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def load_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def load_markdown(md_path: Path) -> str:
    return md_path.read_text(encoding="utf-8")


def load_txt(txt_path: Path) -> str:
    return txt_path.read_text(encoding="utf-8")


def load_document(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".md":
        return load_markdown(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError(f"Format non supporté : {ext}")


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def ingest_all_documents() -> List[Dict]:
    documents = []

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Dossier introuvable : {DATA_DIR}")

    files = list(DATA_DIR.glob("*"))
    files = [f for f in files if f.suffix.lower() in [".pdf", ".md", ".txt"]]

    print(f"📂 {len(files)} fichier(s) trouvé(s) dans {DATA_DIR}")

    for file_path in files:
        print(f"  📄 Traitement de {file_path.name}...")
        try:
            text = load_document(file_path)
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                documents.append({
                    "source": file_path.name,
                    "chunk_id": i,
                    "text": chunk
                })
            print(f"     → {len(chunks)} chunks créés")
        except Exception as e:
            print(f"     ❌ Erreur : {e}")

    print(f"\n✅ Total : {len(documents)} chunks")
    return documents


if __name__ == "__main__":
    docs = ingest_all_documents()
    if docs:
        print("\n--- Exemple de chunk ---")
        print(docs[0]["text"][:300])