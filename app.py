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
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Assistant SAV LVMH",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# STYLE — Contraste corrigé pour mode sombre
# ==========================================
st.markdown("""
<style>
    /* ================================
       HEADERS
       ================================ */
    .main-header {
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #cccccc;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* ================================
       RÉPONSE — fond clair + texte NOIR
       ================================ */
    .answer-box {
        background-color: #e8f4f8;
        color: #1a1a1a !important;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.7;
        font-weight: 500;
    }
    .answer-box * {
        color: #1a1a1a !important;
    }
    
    /* ================================
       SOURCES — fond clair + texte NOIR
       ================================ */
    .source-box {
        background-color: #f8f9fa;
        color: #1a1a1a !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.6rem 0;
        font-size: 0.95rem;
        line-height: 1.5;
        border-left: 4px solid #1f77b4;
    }
    .source-box * {
        color: #1a1a1a !important;
    }
    .source-box b {
        color: #0d47a1 !important;
        font-weight: 600;
    }
    .source-box i {
        color: #555555 !important;
        font-size: 0.9rem;
    }
    
    /* ================================
       HISTORIQUE
       ================================ */
    .history-box {
        background-color: #f0f2f6;
        color: #1a1a1a !important;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        border-left: 3px solid #999;
    }
    .history-box * {
        color: #1a1a1a !important;
    }
    .history-q {
        font-weight: 600;
        color: #0d47a1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<p class="main-header">🛍️ Assistant Service Client LVMH</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Posez vos questions sur les retours, livraisons et commandes</p>',
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    Cet assistant utilise **RAG (Retrieval-Augmented Generation)** 
    pour répondre à vos questions en se basant uniquement sur la 
    documentation interne LVMH.
    
    **Modèle** : Phi (via Ollama)  
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
        "Quel est le prix du sac Birkin ?"  # Test hors sujet
    ]
    for ex in exemples:
        if st.button(ex, use_container_width=True, key=f"btn_{ex}"):
            st.session_state.question = ex

    st.divider()

    if st.button("🗑️ Effacer l'historique", use_container_width=True):
        st.session_state.history = []
        st.success("Historique effacé !")

# ==========================================
# INITIALISATION DU PIPELINE (cachée)
# ==========================================
@st.cache_resource
def init_pipeline():
    """Initialise le pipeline RAG une seule fois."""
    return RAGPipeline()


with st.spinner("🚀 Initialisation de l'assistant..."):
    pipeline = init_pipeline()

# ==========================================
# CHAT
# ==========================================
# Initialiser l'historique
if "history" not in st.session_state:
    st.session_state.history = []

# Champ de saisie
question = st.text_input(
    "💬 Votre question :",
    value=st.session_state.get("question", ""),
    placeholder="Ex : Quel est le délai de retour ?",
    key="input_question"
)

col1, col2 = st.columns([1, 4])
with col1:
    ask = st.button("🔍 Poser la question", type="primary", use_container_width=True)

# Traitement
if ask and question:
    with st.spinner("🤔 Recherche en cours..."):
        result = pipeline.answer(question)

    # Ajouter à l'historique
    st.session_state.history.append({
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    })

    # Afficher la réponse courante
    st.markdown("### 🤖 Réponse")
    st.markdown(
        f'<div class="answer-box">{result["answer"]}</div>',
        unsafe_allow_html=True
    )

    # Afficher les sources
    with st.expander(f"📚 Sources utilisées ({len(result['sources'])})", expanded=True):
        for i, src in enumerate(result["sources"], 1):
            st.markdown(f"""
            <div class="source-box">
                <b>📄 Source {i}</b> : <b>{src['source']}</b> (chunk {src['chunk_id']})<br>
                <b>🎯 Score de pertinence</b> : {src['score']}<br>
                <i>« {src['extrait']} »</i>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# HISTORIQUE DES CONVERSATIONS
# ==========================================
if len(st.session_state.history) > 0:
    st.divider()
    st.markdown(f"### 📜 Historique ({len(st.session_state.history)} question(s))")

    for h in reversed(st.session_state.history[:-1]):  # Exclure la dernière (déjà affichée)
        with st.expander(f"❓ {h['question']}"):
            st.markdown(
                f'<div class="history-box"><span class="history-q">🤖 Réponse :</span> {h["answer"]}</div>',
                unsafe_allow_html=True
            )

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.85rem;">
    Projet RAG LVMH — Démo M2 Data Science | 
    Basé sur <b>Phi (Ollama)</b> · <b>FAISS</b> · <b>Streamlit</b> · <b>MiniLM</b>
</div>
""", unsafe_allow_html=True)