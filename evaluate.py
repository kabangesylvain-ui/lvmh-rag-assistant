"""
Grille d'évaluation de la qualité du pipeline RAG LVMH.
Teste 6 questions : 5 pertinentes + 1 hors sujet.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from rag_pipeline import RAGPipeline
import pandas as pd


# ============================================
# JEU DE TEST
# ============================================
TEST_CASES = [
    {
        "id": 1,
        "question": "Quel est le délai de retour ?",
        "mot_cle": "30 jours",
        "source_attendue": "politique_retour.md",
        "type": "pertinente"
    },
    {
        "id": 2,
        "question": "Combien coûte la livraison ?",
        "mot_cle": "15",
        "source_attendue": "politique_livraison.md",
        "type": "pertinente"
    },
    {
        "id": 3,
        "question": "Comment suivre ma commande ?",
        "mot_cle": "espace client",
        "source_attendue": "faq.md",
        "type": "pertinente"
    },
    {
        "id": 4,
        "question": "Puis-je retourner un article en solde ?",
        "mot_cle": "non",
        "source_attendue": "faq.md",
        "type": "pertinente"
    },
    {
        "id": 5,
        "question": "Quel est le délai de remboursement ?",
        "mot_cle": "14 jours",
        "source_attendue": "politique_retour.md",
        "type": "pertinente"
    },
    {
        "id": 6,
        "question": "Quel est le prix du sac Birkin ?",
        "mot_cle": "pas",  # Doit dire "pas d'information"
        "source_attendue": None,
        "type": "hors_sujet"
    },
]


# ============================================
# FONCTIONS D'ÉVALUATION
# ============================================
def eval_mot_cle(answer: str, mot_cle: str) -> bool:
    """Vérifie que le mot-clé est présent dans la réponse."""
    return mot_cle.lower() in answer.lower()


def eval_source(sources: list, source_attendue: str) -> bool:
    """Vérifie que la source attendue a été récupérée."""
    if source_attendue is None:
        return True  # Pas de source à vérifier pour le hors sujet
    return any(source_attendue in s["source"] for s in sources)


def eval_incertitude(answer: str) -> bool:
    """Vérifie que le LLM admet son incertitude."""
    mots_incertitude = [
        "pas d'information",
        "ne trouve pas",
        "pas mentionné",
        "pas dans la documentation",
        "aucune information",
        "je ne sais pas",
        "pas disponible",
    ]
    return any(mot in answer.lower() for mot in mots_incertitude)


# ============================================
# ÉVALUATION PRINCIPALE
# ============================================
def evaluate():
    print("=" * 70)
    print("📊 GRILLE D'ÉVALUATION DU RAG LVMH")
    print("=" * 70)

    # Initialisation
    print("\n🚀 Chargement du pipeline RAG...")
    pipeline = RAGPipeline()

    print(f"\n🧪 {len(TEST_CASES)} questions à tester\n")
    print("=" * 70)

    results = []

    for test in TEST_CASES:
        print(f"\n[{test['id']}/{len(TEST_CASES)}] ❓ {test['question']}")
        print(f"     🎯 Attendu : {test['mot_cle']}")
        print(f"     📂 Source attendue : {test['source_attendue'] or 'aucune'}")
        print(f"     🏷️  Type : {test['type']}")

        # Appel au pipeline
        result = pipeline.answer(test["question"])
        answer = result["answer"]
        sources = result["sources"]

        # Évaluation
        mot_cle_ok = eval_mot_cle(answer, test["mot_cle"])
        source_ok = eval_source(sources, test["source_attendue"])

        # Évaluation spéciale pour le hors sujet
        if test["type"] == "hors_sujet":
            incertitude_ok = eval_incertitude(answer)
        else:
            incertitude_ok = True  # N/A

        # Affichage
        print(f"     🤖 Réponse : {answer[:200]}{'...' if len(answer) > 200 else ''}")
        print(f"     {'✅' if mot_cle_ok else '❌'} Mot-clé : {'OK' if mot_cle_ok else 'ABSENT'}")
        if test["source_attendue"]:
            print(f"     {'✅' if source_ok else '❌'} Source : {'OK' if source_ok else 'MAUVAISE'}")
        if test["type"] == "hors_sujet":
            print(f"     {'✅' if incertitude_ok else '❌'} Incertitude : {'OK' if incertitude_ok else 'NON ADMISE'}")

        # Score
        if test["type"] == "hors_sujet":
            success = incertitude_ok
        else:
            success = mot_cle_ok and source_ok

        results.append({
            "ID": test["id"],
            "Question": test["question"],
            "Type": test["type"],
            "Mot-clé": "✅" if mot_cle_ok else "❌",
            "Source": "✅" if source_ok else "❌",
            "Incertitude": "✅" if incertitude_ok else "❌" if test["type"] == "hors_sujet" else "—",
            "Réussi": "✅" if success else "❌",
            "Réponse": answer[:150] + "..."
        })

        print("     " + "-" * 50)

    # ============================================
    # RÉSUMÉ FINAL
    # ============================================
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)

    df = pd.DataFrame(results)
    print(df[["ID", "Question", "Type", "Mot-clé", "Source", "Incertitude", "Réussi"]].to_string(index=False))

    # Statistiques
    total = len(results)
    reussites = sum(1 for r in results if r["Réussi"] == "✅")
    mot_cle_ok = sum(1 for r in results if r["Mot-clé"] == "✅")
    source_ok = sum(1 for r in results if r["Source"] == "✅")

    print("\n" + "=" * 70)
    print("📈 MÉTRIQUES")
    print("=" * 70)
    print(f"Réussites globales        : {reussites}/{total} ({reussites / total * 100:.0f}%)")
    print(f"Mots-clés corrects        : {mot_cle_ok}/{total} ({mot_cle_ok / total * 100:.0f}%)")
    print(f"Sources pertinentes       : {source_ok}/{total} ({source_ok / total * 100:.0f}%)")

    # Sauvegarde CSV
    df.to_csv("rapport_evaluation.csv", index=False, encoding="utf-8")
    print(f"\n💾 Rapport sauvegardé : rapport_evaluation.csv")

    # Note globale
    print("\n" + "=" * 70)
    if reussites / total >= 0.8:
        print("🏆 QUALITÉ EXCELLENTE — Le RAG répond correctement")
    elif reussites / total >= 0.6:
        print("👍 QUALITÉ CORRECTE — Quelques améliorations possibles")
    else:
        print("⚠️  QUALITÉ INSUFFISANTE — Revoir le pipeline")
    print("=" * 70)

    return df


if __name__ == "__main__":
    evaluate()