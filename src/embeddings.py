"""
Modèle d'embeddings : convertit du texte en vecteurs.
Utilise sentence-transformers (local, gratuit).
"""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingModel:
    """Wrapper autour de sentence-transformers."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        print(f"🔄 Chargement du modèle : {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_embedding_dimension()
        print(f"✅ Modèle chargé (dimension = {self.dimension})")

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode une liste de textes en vecteurs normalisés."""
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        return embeddings

    def encode_query(self, query: str) -> np.ndarray:
        """Encode une seule requête (pour la recherche)."""
        return self.encode([query])[0]


if __name__ == "__main__":
    model = EmbeddingModel()

    texts = [
        "La politique de retour est de 30 jours.",
        "La livraison prend 2 à 3 jours.",
        "Le remboursement est effectué sous 14 jours."
    ]

    embeddings = model.encode(texts)
    print(f"\n✅ {len(embeddings)} embeddings créés")
    print(f"   Forme : {embeddings.shape}")
    print(f"   Exemple (3 premières valeurs du 1er embedding) :")
    print(f"   {embeddings[0][:3]}")