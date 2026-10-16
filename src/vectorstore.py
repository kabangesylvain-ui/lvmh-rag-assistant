"""
Vector store FAISS : stockage et recherche de similarité.
"""
import pickle
from pathlib import Path
from typing import List, Dict, Tuple

import faiss
import numpy as np

from config import VECTORSTORE_DIR, FAISS_INDEX_NAME, TOP_K


class FaissVectorStore:
    """Wrapper autour de FAISS pour la recherche vectorielle."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = None
        self.documents: List[Dict] = []
        print(f"✅ Vector store initialisé (dimension = {dimension})")

    def build(self, embeddings: np.ndarray, documents: List[Dict]):
        """
        Construit l'index FAISS à partir des embeddings.

        Args:
            embeddings : matrice (n_docs, dimension) normalisée
            documents  : liste de dicts {source, chunk_id, text}
        """
        n_docs = embeddings.shape[0]
        assert n_docs == len(documents), "Incohérence embeddings/documents"

        # Index FAISS avec similarité cosinus (via produit scalaire)
        # car les embeddings sont déjà normalisés
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings.astype(np.float32))
        self.documents = documents

        print(f"✅ Index FAISS créé : {n_docs} documents")

    def search(self, query_embedding: np.ndarray,
               top_k: int = TOP_K) -> List[Tuple[Dict, float]]:
        """
        Recherche les top_k chunks les plus proches de la requête.

        Returns:
            Liste de tuples (document, score_similarité)
        """
        if self.index is None:
            raise ValueError("L'index n'est pas encore construit. Appeler .build() d'abord.")

        # FAISS exige un array 2D
        query = query_embedding.reshape(1, -1).astype(np.float32)

        # Recherche (similarité cosinus, score entre -1 et 1)
        scores, indices = self.index.search(query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:  # FAISS retourne -1 si pas assez de résultats
                results.append((self.documents[idx], float(score)))

        return results

    def save(self, name: str = FAISS_INDEX_NAME):
        """Sauvegarde l'index + les documents sur disque."""
        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

        index_path = VECTORSTORE_DIR / f"{name}.faiss"
        docs_path = VECTORSTORE_DIR / f"{name}_docs.pkl"

        faiss.write_index(self.index, str(index_path))
        with open(docs_path, "wb") as f:
            pickle.dump(self.documents, f)

        print(f"✅ Index sauvegardé : {index_path}")
        print(f"✅ Documents sauvegardés : {docs_path}")

    def load(self, name: str = FAISS_INDEX_NAME):
        """Charge l'index + les documents depuis le disque."""
        index_path = VECTORSTORE_DIR / f"{name}.faiss"
        docs_path = VECTORSTORE_DIR / f"{name}_docs.pkl"

        if not index_path.exists():
            raise FileNotFoundError(f"Index introuvable : {index_path}")

        self.index = faiss.read_index(str(index_path))
        with open(docs_path, "rb") as f:
            self.documents = pickle.load(f)

        print(f"✅ Index chargé : {len(self.documents)} documents")


if __name__ == "__main__":
    # Test end-to-end : ingestion + embeddings + index + recherche
    from ingestion import ingest_all_documents
    from embeddings import EmbeddingModel

    print("=== ÉTAPE 1 : Ingestion ===")
    documents = ingest_all_documents()

    print("\n=== ÉTAPE 2 : Embeddings ===")
    model = EmbeddingModel()
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts)

    print("\n=== ÉTAPE 3 : Index FAISS ===")
    store = FaissVectorStore(dimension=model.dimension)
    store.build(embeddings, documents)

    print("\n=== ÉTAPE 4 : Test de recherche ===")
    query = "Quel est le délai de retour ?"
    print(f"Requête : « {query} »\n")

    query_emb = model.encode_query(query)
    results = store.search(query_emb, top_k=3)

    for i, (doc, score) in enumerate(results, 1):
        print(f"--- Résultat {i} (score = {score:.4f}) ---")
        print(f"Source : {doc['source']} (chunk {doc['chunk_id']})")
        print(f"Texte  : {doc['text'][:200]}...")
        print()