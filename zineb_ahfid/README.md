# Assistant Technique Intelligent – Auto-Correcteur

## 1. Présentation du projet

Ce projet consiste à développer un assistant technique intelligent capable de répondre aux questions des utilisateurs concernant les erreurs informatiques.

L'assistant utilise un Large Language Model (LLM) via l'API OpenRouter afin de générer des réponses structurées et compréhensibles.

## 2. Objectifs

- Analyser les questions techniques des utilisateurs.
- Identifier les erreurs informatiques.
- Proposer un diagnostic.
- Fournir des solutions et des actions correctives.
- Générer des réponses au format JSON.
- Étudier l'influence du paramètre Temperature sur les réponses du modèle.

## 3. Technologies utilisées

- Python
- OpenRouter API
- Large Language Models (LLM)
- JSON
- PowerShell
- Git & GitHub

## 4. Fonctionnalités

- Communication avec un modèle LLM via OpenRouter.
- Configuration de la clé API à travers une variable d'environnement.
- Génération de réponses structurées.
- Diagnostic des erreurs techniques.
- Comparaison des réponses selon différentes valeurs de Temperature.
- Gestion de l'historique des conversations (5 derniers échanges).

## 5. Difficultés rencontrées et solutions

### Difficulté 1 : Configuration de la clé API

**Problème :** Comprendre comment créer et configurer une clé API pour communiquer avec OpenRouter.

**Solution :** Création d'une clé API et configuration de la variable d'environnement `LLM_KEY`.

### Difficulté 2 : Configuration de l'API OpenRouter

**Problème :** Comprendre la différence entre la clé API, l'URL de base et le nom du modèle.

**Solution :** Configuration des variables suivantes :
- `LLM_KEY`
- `BASE_URL`
- `MODEL`

### Difficulté 3 : Exécution du programme

**Problème :** Comprendre comment lancer le script Python depuis le terminal.

**Solution :** Utilisation de la commande :

```bash
python assistant_corrige.py
```

### Difficulté 4 : Structuration des réponses

**Problème :** Obtenir des réponses claires et organisées sous forme de JSON.

**Solution :** Utilisation d'instructions précises dans le prompt pour structurer les réponses.

### Difficulté 5 : Compréhension du paramètre Temperature

**Problème :** Comprendre son influence sur la génération des réponses.

**Solution :** Préparation d'une comparaison entre plusieurs valeurs de Temperature, notamment 0.0 et 1.2.

## 6. Installation et exécution

### Prérequis

- Python installé.
- Une clé API OpenRouter.

### Configuration

Configurer les variables d'environnement :

```powershell
$env:LLM_KEY="YOUR_API_KEY"
$env:BASE_URL="https://openrouter.ai/api/v1"
$env:MODEL="openrouter/free"
```

### Lancement

```bash
python assistant_corrige.py
```

## 7. Exemple d'utilisation

**Question :**

Que signifie une erreur HTTP 404 ?

**Résultat attendu :**

Une réponse structurée contenant :
- Diagnostic
- Gravité
- Action corrective

## 8. Sécurité

La clé API est stockée dans une variable d'environnement et ne doit jamais être publiée sur GitHub.

## 9. Conclusion

Ce projet permet de découvrir l'intégration des Large Language Models dans une application Python, la communication avec une API externe et la génération de réponses structurées pour l'assistance technique.
