"""
Configuration centralisée du projet RAG LVMH.
"""
from pathlib import Path

# ==========================================
# CHEMINS
# ==========================================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
ASSETS_DIR = BASE_DIR / "assets"

# ==========================================
# INGESTION
# ==========================================
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ==========================================
# EMBEDDINGS
# ==========================================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================================
# VECTOR STORE
# ==========================================
FAISS_INDEX_NAME = "lvmh_index"

# ==========================================
# RETRIEVAL
# ==========================================
TOP_K = 3

# ==========================================
# LLM
# ==========================================
LLM_PROVIDER = "ollama"
LLM_MODEL = "llama3.2:3b"

# ==========================================
# PROMPT
# ==========================================
SYSTEM_PROMPT = """Tu es un assistant du service après-vente de LVMH.
Réponds de manière courtoise, précise et professionnelle.

RÈGLES :
- Base-toi UNIQUEMENT sur le contexte fourni.
- Si l'information n'est pas dans le contexte, dis-le clairement.
- Ne jamais inventer de politique, de délai ou de tarif.
- Cite tes sources quand c'est pertinent.
"""

USER_PROMPT_TEMPLATE = """CONTEXTE :
{context}

QUESTION :
{question}

Réponds à la question en te basant uniquement sur le contexte ci-dessus.
Si l'information n'y figure pas, indique que tu ne peux pas répondre."""