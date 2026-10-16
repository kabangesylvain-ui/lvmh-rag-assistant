# 📊 Rapport de synthèse — Assistant RAG LVMH

## 📋 Table des matières

1. [Résumé exécutif](#1-résumé-exécutif)
2. [Contexte et problématique](#2-contexte-et-problématique)
3. [Démarche technique](#3-démarche-technique)
4. [Résultats](#4-résultats)
5. [Limites identifiées](#5-limites-identifiées)
6. [Risques et biais](#6-risques-et-biais)
7. [Recommandations](#7-recommandations)
8. [Conclusion](#8-conclusion)

---

## 1. Résumé exécutif

### Mission

Automatiser le service après-vente LVMH via un assistant conversationnel basé sur RAG (Retrieval-Augmented Generation).

### Résultats clés

| Métrique | Valeur |
|---|---|
| **Questions testées** | 6 (5 pertinentes + 1 hors sujet) |
| **Taux de réussite** | **100 %** |
| **Hallucinations** | 0 |
| **Modèle retenu** | llama3.2:3b (Ollama) |
| **Coût** | Gratuit (100 % local) |

### Livrables

- ✅ Assistant RAG fonctionnel (Streamlit)
- ✅ Pipeline Python modulaire
- ✅ Grille d'évaluation (100 % de réussite)
- ✅ Documentation complète

---

## 2. Contexte et problématique

### Contexte

| Élément | Détail |
|---|---|
| **Entreprise** | Accenture (client LVMH) |
| **Domaine** | Service après-vente |
| **Problème** | Volume élevé d'emails/messages clients |
| **Objectif** | Automatiser 80 % des réponses |

### Problématique

> **Comment construire un assistant conversationnel fiable qui répond aux questions fréquentes des clients LVMH, en se basant uniquement sur la documentation interne, sans halluciner ?**

### Enjeux

| Enjeu | Impact |
|---|---|
| **Efficacité** | Réduire la charge du SAV |
| **Qualité** | Réponses cohérentes avec la politique LVMH |
| **Confidentialité** | Données sensibles → solution locale |
| **Coût** | Solution gratuite (pas d'API) |

---

## 3. Démarche technique

### Architecture RAG

Le **RAG (Retrieval-Augmented Generation)** combine :

1. **Retrieval** : recherche des passages pertinents
2. **Generation** : génération de la réponse par un LLM

### Étapes

| Étape | Composant | Rôle |
|---|---|---|
| 1 | **Ingestion** | Chargement + découpage (500 caractères) |
| 2 | **Embeddings** | Conversion en vecteurs (MiniLM, 384 dim) |
| 3 | **FAISS** | Indexation + recherche similarité |
| 4 | **Retrieval** | Récupération des 3 meilleurs chunks |
| 5 | **LLM** | Génération (llama3.2:3b) |

### Choix techniques

| Choix | Justification |
|---|---|
| **Ollama (local)** | Confidentialité, gratuité |
| **FAISS** | Rapide, gratuit, standard |
| **MiniLM-L6-v2** | Léger, performant (384 dim) |
| **Streamlit** | Interface web simple |

### Prompt engineering

Le **prompt système** impose des règles strictes :

```
- Base-toi UNIQUEMENT sur le contexte fourni
- Ne JAMAIS inventer
- Admets ton incertitude
- Réponds en 1-3 phrases
```

---

## 4. Résultats

### Grille d'évaluation

| # | Question | Type | Résultat |
|---|---|---|---|
| 1 | Délai de retour | Pertinente | ✅ |
| 2 | Coût livraison | Pertinente | ✅ |
| 3 | Suivi commande | Pertinente | ✅ |
| 4 | Article en solde | Pertinente | ✅ |
| 5 | Délai remboursement | Pertinente | ✅ |
| 6 | Prix du sac Birkin | Hors sujet | ✅ |

**Score : 6/6 (100 %)**

### Comparaison des modèles LLM

| Modèle | Taille | Score | Recommandation |
|---|---|---|---|
| **llama3.2:3b** | 2.0 Go | 6/6 (100 %) | ✅ Retenu |
| **phi** | 1.6 Go | 1/6 (17 %) | ❌ Trop faible |

### Exemples de réponses

**Question 1** : "Quel est le délai de retour ?"

> *"D'après la politique de retour LVMH, le délai de retour est de 30 jours à compter de la date de réception de l'article."*

✅ **Correct** + citation de la source

**Question 6** : "Quel est le prix du sac Birkin ?"

> *"Je suis désolé, mais je n'ai pas d'informations sur le prix du sac Birkin dans le contexte fourni."*

✅ **Admet l'incertitude** → pas d'hallucination

---

## 5. Limites identifiées

### Limites techniques

| Limite | Impact | Mitigation |
|---|---|---|
| **Lenteur sur CPU** | 30-60 sec / question | GPU en production |
| **Base documentaire limitée** | 3 documents seulement | Enrichir la base |
| **Chunking fixe** | 500 caractères | Chunking sémantique |
| **Un seul LLM** | Dépendance à llama3.2:3b | Fallback multi-modèles |

### Limites fonctionnelles

| Limite | Description |
|---|---|
| **Pas d'historique de conversation** | Chaque question est indépendante |
| **Pas de multilingue** | Réponses uniquement en français |
| **Pas d'escalade humaine** | Impossible de transférer au SAV |
| **Pas d'authentification** | Pas de vérification client |

### Limites des données

- **Dataset simulé** : 3 documents Markdown seulement
- **Pas de cas réels** : pas d'emails clients authentiques
- **Pas de feedback** : pas d'apprentissage continu

---

## 6. Risques et biais

### Risques d'hallucination

| Risque | Mitigation en place |
|---|---|
| **Inventer une réponse** | Prompt strict + score minimum |
| **Confondre les sources** | Citation obligatoire |
| **Ignorer le contexte** | Test sur 6 questions |

**Résultat** : **0 hallucination détectée** ✅

### Biais potentiels

| Biais | Description | Mitigation |
|---|---|---|
| **Biais linguistique** | Modèle entraîné en anglais | Prompt en français |
| **Biais documentaire** | Basé sur 3 docs | Enrichir la base |
| **Biais de génération** | LLM peut préférer certaines formulations | Diversifier les tests |

### Risques de sécurité

| Risque | Niveau | Mitigation |
|---|---|---|
| **Fuite de données** | 🟢 Faible (100 % local) | Pas d'API externe |
| **Injection de prompt** | 🟡 Moyen | Validation des entrées |
| **Accès non autorisé** | 🟡 Moyen | Authentification à ajouter |

---

## 7. Recommandations

### Court terme (0-1 mois)

| # | Action | Priorité |
|---|---|---|
| 1 | **Enrichir la base documentaire** (10+ documents) | 🔴 Haute |
| 2 | **Ajouter l'authentification** client | 🔴 Haute |
| 3 | **Tester avec plus de questions** (50+) | 🟡 Moyenne |

### Moyen terme (1-3 mois)

| # | Action | Priorité |
|---|---|---|
| 4 | **Déployer sur GPU** (Ollama GPU) | 🔴 Haute |
| 5 | **Ajouter un historique** de conversation | 🟡 Moyenne |
| 6 | **Intégrer au SAV existant** (API) | 🟡 Moyenne |

### Long terme (3-6 mois)

| # | Action | Priorité |
|---|---|---|
| 7 | **Fine-tuning** d'un modèle LVMH | 🟡 Moyenne |
| 8 | **Feedback loop** (apprentissage continu) | 🟢 Basse |
| 9 | **Multilingue** (EN, IT, ZH) | 🟢 Basse |

### Architecture cible

```
┌─────────────────────────────────────────┐
│  Chatbot web (Streamlit)                │
├─────────────────────────────────────────┤
│  API REST (FastAPI)                     │
├─────────────────────────────────────────┤
│  RAG Pipeline                           │
│  ├─ Embeddings (GPU)                    │
│  ├─ FAISS (10k+ docs)                   │
│  └─ LLM (llama3.1:8b ou mistral)        │
├─────────────────────────────────────────┤
│  Base documentaire LVMH enrichie        │
├─────────────────────────────────────────┤
│  Monitoring + Feedback                  │
└─────────────────────────────────────────┘
```

---

## 8. Conclusion

### Bilan

Ce projet a permis de construire un **assistant RAG complet** pour le service après-vente LVMH, avec :

- ✅ **100 % de réussite** sur les tests
- ✅ **0 hallucination**
- ✅ **100 % local** (confidentialité)
- ✅ **Solution gratuite** (pas d'API)

### Valeur ajoutée

| Aspect | Valeur |
|---|---|
| **Technique** | Maîtrise complète du RAG |
| **Business** | Automatisation du SAV |
| **Éthique** | Confidentialité préservée |

### Perspectives

L'assistant peut être **industrialisé** avec :

1. **GPU** → 10× plus rapide
2. **Base enrichie** → 10× plus de couverture
3. **Authentification** → conformité RGPD

### Compétences démontrées

- ✅ **RAG** : architecture complète
- ✅ **Vector Search** : FAISS
- ✅ **LLM** : Ollama, llama3.2:3b
- ✅ **Prompt engineering**
- ✅ **Évaluation** : grille de qualité
- ✅ **Déploiement** : Streamlit

---

## 📎 Annexes

- **Annexe A** : Code source (`src/*.py`)
- **Annexe B** : Documents LVMH (`data/*.md`)
- **Annexe C** : Résultats des tests (`rapport_evaluation.csv`)
- **Annexe D** : Interface (`app.py`)

---

**Auteur** : KABANGE MBUYA SYLVAIN
**Date** : Octobre 2026  
**Projet** : Data Science — Projet 3
**Entreprise** : Accenture (client LVMH)