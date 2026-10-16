# 🛍️ Assistant RAG LVMH — Service Après-Vente

> **Assistant conversationnel** basé sur RAG (Retrieval-Augmented Generation) pour automatiser les réponses du service client LVMH.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2:3b-black)](https://ollama.ai/)
[![FAISS](https://img.shields.io/badge/Vector_Store-FAISS-blue)](https://github.com/facebookresearch/faiss)
[![Qualité RAG](https://img.shields.io/badge/Qualité_RAG-100%25-success)](.)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Table des matières

- [🎯 Objectif](#-objectif)
- [📊 Résultats](#-résultats)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Stack technique](#️-stack-technique)
- [📸 Aperçu de l'interface](#-aperçu-de-linterface)
- [🚀 Installation](#-installation)
- [🎬 Utilisation](#-utilisation)
- [📊 Évaluation](#-évaluation)
- [📁 Structure du projet](#-structure-du-projet)
- [🎓 Compétences mobilisées](#-compétences-mobilisées)
- [👤 Auteur](#-auteur)

---

## 🎯 Objectif

Automatiser le **service après-vente LVMH** en répondant automatiquement aux questions fréquentes des clients sur :

- 📦 **Retours** (délais, conditions, frais)
- 🚚 **Livraisons** (délais, tarifs, suivi)
- 💬 **FAQ** (suivi commande, remboursement, modifications)

**Contexte** : Projet Data Science M2 — Accenture (client LVMH)

---

## 📊 Résultats

### Qualité du RAG (100 % de réussite)

| Métrique | Score |
|---|---|
| **Réussites globales** | **6/6 (100 %)** |
| **Mots-clés corrects** | **6/6 (100 %)** |
| **Sources pertinentes** | **6/6 (100 %)** |
| **Pas d'hallucination** | ✅ Confirmé |

### Comparaison des modèles LLM

| Modèle | Taille | Score RAG |
|---|---|---|
| 🥇 **llama3.2:3b** | 2.0 Go | **6/6 (100 %)** |
| 🥈 phi | 1.6 Go | 1/6 (17 %) |

🏆 **Modèle retenu** : **llama3.2:3b** via Ollama

### Performances

- ⚡ **Temps de réponse** : ~30-60 sec / question (CPU)
- 💾 **Mémoire** : ~2 Go pour le modèle
- 🌐 **100 % local** : aucune donnée ne sort de la machine

![Métriques d'évaluation](assets/03_metrique.png)

---

## 🏗️ Architecture

```
┌──────────────────────┐
│  Question client     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Embedding (MiniLM)  │  ← Conversion texte → vecteur
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  FAISS Vector Store  │  ← Recherche similarité
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Contexte + Question │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  LLM (llama3.2:3b)   │  ← Génération réponse
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Réponse + Sources   │
└──────────────────────┘
```

![Pipeline RAG](assets/05_pipeline_rag.png)

### Pipeline RAG

1. **Ingestion** : Découpage des documents LVMH en chunks
2. **Embedding** : Conversion des chunks en vecteurs (MiniLM 384 dim)
3. **Indexation** : Stockage dans FAISS
4. **Recherche** : Matching question ↔ chunks pertinents
5. **Génération** : LLM produit une réponse fondée sur le contexte

---

## 🛠️ Stack technique

| Catégorie | Technologies |
|---|---|
| **Langage** | Python 3.11 |
| **LLM local** | Ollama + `llama3.2:3b` |
| **Embeddings** | `sentence-transformers` (MiniLM-L6-v2) |
| **Vector Store** | FAISS (Facebook AI) |
| **Interface** | Streamlit |
| **Parsing** | pypdf |
| **Config** | python-dotenv |

---

## 📸 Aperçu de l'interface

### 🖥️ Interface principale

![Interface Streamlit](assets/01_affiche.png)

### 💬 Exemple de question — Délai de retour

![Question 1](assets/06_question1.png)

### 📚 Sources utilisées

![Sources](assets/15_sources.png)

### 🎯 Toutes les questions testées

| Question | Aperçu |
|---|---|
| Q1 — Délai de retour | ![Q1](assets/09_question1.png) |
| Q2-Q3 — Livraison & Suivi | ![Q2-3](assets/10_question2_3.png) |
| Q4-Q5 — Soldes & Remboursement | ![Q4-5](assets/11_question4_5.png) |
| Q6 — Hors sujet (Birkin) | ![Q6](assets/12_question6.png) |

### 📄 Rapport de synthèse

![Rapport](assets/16_rapport.png)

### 📊 Résultats d'évaluation

![Rapports](assets/17_rapports.png)

### 🛠️ Service client

![Service](assets/14_service.png)

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- [Ollama](https://ollama.ai/download) installé
- 4 Go de RAM minimum

### 1. Cloner le repo

```bash
git clone https://github.com/kabangesylvain-ui/lvmh-rag-assistant.git
cd lvmh-rag-assistant
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger le modèle LLM

```bash
ollama pull llama3.2:3b
```

### 5. Configurer Hugging Face (optionnel)

Crée un fichier `.env` :

```
HF_TOKEN=hf_votre_token_ici
```

### 6. Indexer les documents

```bash
cd src
python ingestion.py
cd ..
```

---

## 🎬 Utilisation

### Interface Streamlit

```bash
streamlit run app.py
```

→ Ouvre **http://localhost:8501**

**Exemples de questions** :

- "Quel est le délai de retour ?"
- "Combien coûte la livraison ?"
- "Comment suivre ma commande ?"
- "Puis-je retourner un article en solde ?"
- "Quel est le délai de remboursement ?"

### Pipeline en ligne de commande

```bash
cd src
python rag_pipeline.py
```

---

## 📊 Évaluation

### Lancer la grille d'évaluation

```bash
python evaluate.py
```

**Résultat attendu** :

```
📈 MÉTRIQUES
======================================================
Réussites globales        : 6/6 (100%)
Mots-clés corrects        : 6/6 (100%)
Sources pertinentes       : 6/6 (100%)

🏆 QUALITÉ EXCELLENTE
```

### Jeu de test

| # | Question | Réponse attendue | Type |
|---|---|---|---|
| 1 | Quel est le délai de retour ? | 30 jours | Pertinente |
| 2 | Combien coûte la livraison ? | 15 € ou gratuit | Pertinente |
| 3 | Comment suivre ma commande ? | Espace client | Pertinente |
| 4 | Puis-je retourner un article en solde ? | Non | Pertinente |
| 5 | Quel est le délai de remboursement ? | 14 jours | Pertinente |
| 6 | Quel est le prix du sac Birkin ? | Pas d'info | Hors sujet |

### Critères d'évaluation

- ✅ **Exactitude** : le mot-clé attendu est dans la réponse
- ✅ **Retrieval** : le bon document source est récupéré
- ✅ **Incertitude** : le LLM admet quand il ne sait pas

---

## 📁 Structure du projet

```
LVMH_RAG_Assistant/
│
├── 📁 src/                          # Modules Python
│   ├── config.py                    # Configuration
│   ├── ingestion.py                 # Chargement + chunking
│   ├── embeddings.py                # Modèle d'embeddings
│   ├── vectorstore.py               # FAISS
│   ├── llm.py                       # Client Ollama
│   └── rag_pipeline.py              # Pipeline RAG
│
├── 📁 data/                         # Documents LVMH
│   ├── politique_retour.md
│   ├── politique_livraison.md
│   └── faq.md
│
├── 📁 vectorstore/                  # Index FAISS
│   ├── lvmh_index.faiss
│   └── lvmh_index_docs.pkl
│
├── 📁 assets/                       # Captures d'écran (17 images)
│   ├── 01_affiche.png
│   ├── 02_articles.png
│   ├── ...
│   └── 17_rapports.png
│
├── 📁 .streamlit/
│   └── config.toml                  # Thème Streamlit
│
├── 📄 app.py                        # Interface Streamlit
├── 📄 evaluate.py                   # Grille d'évaluation
├── 📄 requirements.txt              # Dépendances
├── 📄 .env                          # Tokens (non versionné)
├── 📄 .gitignore
├── 📄 README.md                     # Ce fichier
├── 📄 RAPPORT.md                    # Analyse détaillée
└── 📄 rapport_evaluation.csv        # Résultats des tests
```

---

## 🎯 Impact business

| Indicateur | Valeur |
|---|---|
| **Questions automatisables** | ~80 % du SAV |
| **Temps de réponse** | < 1 min vs plusieurs heures |
| **Disponibilité** | 24h/24, 7j/7 |
| **Confidentialité** | 100 % local |
| **Coût** | Gratuit (pas d'API) |

---

## 🎓 Compétences mobilisées

- ✅ **RAG** : Retrieval-Augmented Generation
- ✅ **Embeddings** : sentence-transformers
- ✅ **Vector Search** : FAISS
- ✅ **LLM local** : Ollama
- ✅ **Prompt engineering**
- ✅ **Streamlit** : interface web
- ✅ **Évaluation** : grille de qualité RAG

---

## 📄 License

MIT License.

---

## 👤 Auteur

**KABANGE MBUYA SYLVAIN**

🎓 Data Science — Horizon University  
📧 kabange.sylvain@horizon-university.tn  
🔗 [GitHub @kabangesylvain-ui](https://github.com/kabangesylvain-ui)

---

⭐ **Si ce projet vous a plu, n'hésitez pas à lui donner une étoile !**