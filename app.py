"""
Interface Streamlit pour l'assistant RAG LVMH.
"""
import streamlit as st
import sys
from pathlib import Path

# Ajouter src/ au PYTHONPATH
sys.path.append(str(Path(__file__).parent / "src"))

from rag_pipeline import RAGPipeline

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Assistant SAV LVMH",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================
st.title("🛍️ Assistant Service Client LVMH")
st.caption("Posez vos questions sur les retours, livraisons et commandes")

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    Cet assistant utilise **RAG (Retrieval-Augmented Generation)** 
    pour répondre à vos questions en se basant uniquement sur la 
    documentation interne LVMH.
    
    **Modèle** : llama3.2:3b (via Ollama)  
    **Base vectorielle** : FAISS  
    **Embeddings** : MiniLM-L6-v2
    """)

    st.divider()

    st.header("💡 Exemples de questions")
    exemples = [
        "Quel est le délai de retour ?",
        "Combien coûte la livraison ?",
        "Comment suivre ma commande ?",
        "Puis-je retourner un article en solde ?",
        "Quel est le délai de remboursement ?",
        "Quel est le prix du sac Birkin ?"
    ]
    for ex in exemples:
        if st.button(ex, use_container_width=True, key=f"btn_{ex}"):
            st.session_state.question = ex

    st.divider()
    if st.button("🗑️ Effacer l'historique", use_container_width=True):
        st.session_state.history = []
        st.success("Historique effacé !")

# ==========================================
# INITIALISATION DU PIPELINE
# ==========================================
@st.cache_resource
def init_pipeline():
    return RAGPipeline()

with st.spinner("🚀 Initialisation de l'assistant..."):
    pipeline = init_pipeline()

# ==========================================
# CHAT
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

# Champ de saisie
question = st.text_input(
    "💬 Votre question :",
    value=st.session_state.get("question", ""),
    placeholder="Ex : Quel est le délai de retour ?",
    key="input_question"
)

if st.button("🔍 Poser la question", type="primary"):
    if question:
        with st.spinner("🤔 Recherche en cours... (patience ~30 sec)"):
            result = pipeline.answer(question)

        # Historique
        st.session_state.history.append({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        })

        # Réponse (style natif, pas de bug React)
        st.subheader("🤖 Réponse")
        st.success(result["answer"])

        # Sources
        st.subheader("📚 Sources utilisées")
        for i, src in enumerate(result["sources"], 1):
            with st.expander(f"📄 Source {i} : {src['source']} (chunk {src['chunk_id']})"):
                st.write(f"**Score de pertinence** : {src['score']}")
                st.caption(f"_{src['extrait']}_")
    else:
        st.warning("⚠️ Veuillez poser une question.")

# ==========================================
# HISTORIQUE
# ==========================================
if len(st.session_state.history) > 1:
    st.divider()
    st.subheader(f"📜 Historique ({len(st.session_state.history) - 1} question(s))")
    for h in reversed(st.session_state.history[:-1]):
        with st.expander(f"❓ {h['question']}"):
            st.info(h["answer"])

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("Projet RAG LVMH — Démo M2 Data Science | Basé sur Phi · FAISS · Streamlit · Ollama")