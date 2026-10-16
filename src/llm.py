"""
Connexion au LLM : Ollama (local) ou OpenAI.
"""
from config import LLM_PROVIDER, LLM_MODEL, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class LLMClient:
    """Client LLM unifié (Ollama ou OpenAI)."""

    def __init__(self, provider: str = LLM_PROVIDER, model: str = LLM_MODEL):
        self.provider = provider
        self.model = model

        if provider == "ollama":
            from ollama import Client
            self.client = Client()
            print(f"✅ LLM Ollama prêt (modèle = {model})")
        elif provider == "openai":
            from openai import OpenAI
            self.client = OpenAI()
            print(f"✅ LLM OpenAI prêt (modèle = {model})")
        else:
            raise ValueError(f"Provider inconnu : {provider}")

    def generate(self, question: str, context: str) -> str:
        """Génère une réponse à partir de la question et du contexte."""
        print("📤 Préparation de la requête...")

        user_prompt = USER_PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )

        if self.provider == "ollama":
            print(f"⏳ Envoi à Ollama (modèle = {self.model})...")
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ]
            )
            print("✅ Réponse reçue !")
            return response["message"]["content"]

        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEST DU LLM")
    print("=" * 60)

    client = LLMClient()

    question = "Quel est le délai de retour ?"
    context = """# Politique de retour LVMH

## Délai de retour
Les clients disposent de 30 jours à compter de la date de réception
pour retourner un article, sans justification."""

    print(f"\n❓ Question : {question}")
    print(f"\n📄 Contexte :\n{context}")
    print(f"\n⏳ Génération de la réponse...\n")

    answer = client.generate(question, context)

    print(f"\n🤖 Réponse :\n{answer}")
    print("\n" + "=" * 60)