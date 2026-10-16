"""
Pipeline RAG complet : question → réponse augmentée.
"""
from typing import Dict, List
from ingestion import ingest_all_documents
from embeddings import EmbeddingModel
from vectorstore import FaissVectorStore
from llm import LLMClient
from config import TOP_K


class RAGPipeline:
    """Pipeline RAG end-to-end."""

    def __init__(self, load_existing: bool = True):
        print("=" * 60)
        print("🚀 INITIALISATION DU PIPELINE RAG")
        print("=" * 60)

        self.embedder = EmbeddingModel()
        self.store = FaissVectorStore(dimension=self.embedder.dimension)

        try:
            if load_existing:
                self.store.load()
                print("✅ Index FAISS chargé depuis le disque")
        except FileNotFoundError:
            print("⚠️  Aucun index trouvé, construction en cours...")
            self.build_index()

        self.llm = LLMClient()

        print("=" * 60)
        print("✅ Pipeline RAG prêt")
        print("=" * 60)

    def build_index(self):
        print("\n📥 Ingestion des documents...")
        documents = ingest_all_documents()

        print("\n🔢 Création des embeddings...")
        texts = [doc["text"] for doc in documents]
        embeddings = self.embedder.encode(texts)

        print("\n💾 Construction de l'index FAISS...")
        self.store.build(embeddings, documents)
        self.store.save()

    def retrieve(self, question: str, top_k: int = TOP_K) -> List[Dict]:
        query_emb = self.embedder.encode_query(question)
        results = self.store.search(query_emb, top_k=top_k)
        return [{"doc": doc, "score": score} for doc, score in results]

    def answer(self, question: str, top_k: int = TOP_K) -> Dict:
        print(f"\n🔍 Recherche des chunks pertinents...")
        results = self.retrieve(question, top_k=top_k)
        print(f"✅ {len(results)} chunks trouvés")

        context_parts = []
        sources = []
        for r in results:
            doc = r["doc"]
            context_parts.append(
                f"[Source : {doc['source']} | chunk {doc['chunk_id']}]\n{doc['text']}"
            )
            sources.append({
                "source": doc["source"],
                "chunk_id": doc["chunk_id"],
                "score": round(r["score"], 4),
                "extrait": doc["text"][:150] + "..."
            })

        context = "\n\n".join(context_parts)
        
        print(f"🤖 Appel au LLM...")
        answer = self.llm.generate(question, context)

        return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    pipeline = RAGPipeline()

    # Test avec 1 seule question d'abord (pour aller vite)
    question = "Quel est le délai de retour ?"
    
    print("\n" + "=" * 60)
    print(f"❓ {question}")
    print("=" * 60)
    
    result = pipeline.answer(question)
    
    print(f"\n🤖 Réponse :\n{result['answer']}")
    print(f"\n📚 Sources :")
    for src in result["sources"]:
        print(f"   - {src['source']} (chunk {src['chunk_id']}, score {src['score']})")