
import json
import os
from openai import APIConnectionError, APIError, OpenAI

BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL = os.environ.get("MODEL")

MAX_ECHANGES = 5

SYSTEM_PROMPT = """
Tu es un assistant de diagnostic technique informatique.

Réponds uniquement par un objet JSON valide,
sans Markdown ni texte autour.

Le JSON doit contenir exactement trois champs de type chaîne :
- diagnostic
- gravite
- action

Distingue les hypothèses et les certitudes.
Si les données sont insuffisantes, indique-le.
Ne propose pas de commande destructive sans avertissement.
"""


def appel(client, messages, temperature):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=300
    )


def texte_de(reponse):
    if not reponse.choices:
        raise ValueError("La passerelle ne renvoie aucun choix.")

    choix = reponse.choices[0]

    if choix.finish_reason == "length":
        raise ValueError("Réponse tronquée.")

    if not choix.message.content:
        raise ValueError("Réponse vide.")

    return choix.message.content


def afficher_usage(reponse):
    usage = reponse.usage

    if usage is None:
        print("Tokens : information non fournie.")
    else:
        print(f"Tokens entrée : {usage.prompt_tokens}")
        print(f"Tokens sortie : {usage.completion_tokens}")
        print(f"Tokens total : {usage.total_tokens}")


def valider_json(texte):
    donnees = json.loads(texte)

    champs = {"diagnostic", "gravite", "action"}

    if not isinstance(donnees, dict) or set(donnees) != champs:
        raise ValueError("Les trois champs sont obligatoires.")

    if not all(isinstance(donnees[c], str) for c in champs):
        raise ValueError("Les valeurs doivent être des chaînes.")

    return donnees


def demonstrations(client):

    tests = [
        ("Premier appel", "Que signifie une erreur HTTP 404 ?", 0.0),
        ("Temperature 0.0",
         "Propose trois pistes pour diagnostiquer un serveur web lent.",
         0.0),
        ("Temperature 1.2",
         "Propose trois pistes pour diagnostiquer un serveur web lent.",
         1.2)
    ]

    for titre, question, temperature in tests:
        print(f"\n=== {titre} ===")

        try:
            reponse = appel(
                client,
                [{"role": "user", "content": question}],
                temperature
            )

            print(texte_de(reponse))
            print("Modèle :", reponse.model)
            afficher_usage(reponse)

        except (APIConnectionError, APIError, ValueError) as erreur:
            print("Erreur :", erreur)


def assistant_cli(client):

    historique = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("\n=== Assistant technique ===")
    print("Tapez 'quitter' pour terminer.")

    while True:
        try:
            probleme = input("\nVous : ").strip()

        except (EOFError, KeyboardInterrupt):
            break

        if probleme.lower() == "quitter":
            break

        if not probleme:
            continue

        historique.append({
            "role": "user",
            "content": probleme
        })

        try:
            reponse = appel(
                client,
                historique,
                temperature=0.0
            )

            texte = texte_de(reponse)
            diagnostic = valider_json(texte)

        except (APIConnectionError, APIError, ValueError) as erreur:
            historique.pop()
            print("Erreur :", erreur)
            continue

        historique.append({
            "role": "assistant",
            "content": texte
        })

        historique = [
            historique[0]
        ] + historique[1:][-2 * MAX_ECHANGES:]

        print("\nAssistant :")
        print(json.dumps(
            diagnostic,
            ensure_ascii=False,
            indent=2
        ))

        afficher_usage(reponse)

    print("Fin de la conversation.")


def main():

    if not BASE_URL or not API_KEY or not MODEL:
        raise SystemExit(
            "Définissez BASE_URL, API_KEY et MODEL."
        )

    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
        timeout=60.0
    )

    demonstrations(client)
    assistant_cli(client)


if __name__ == "__main__":
    main()
