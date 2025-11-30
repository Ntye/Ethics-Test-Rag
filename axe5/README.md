
## 📘 README.md — axe5

```markdown
# ⚖️ axe5 — Système RAG Juridique (API Backend)

Ce projet fournit un backend API pour interroger un système RAG (Retrieval-Augmented Generation) appliqué au domaine juridique.
Il permet de poser des questions via des requêtes HTTP et d’obtenir des réponses au format JSON.

---

## 🚀 Installation

### 1. 📦 Prérequis

- Python 3.10+
- Git
- Conda ou venv (environnement virtuel recommandé)

### 2. 🛠️ Cloner le projet

```bash
git clone https://github.com/armelkoudjou/axe5.git
cd axe5
```

### 3. ⚙️ Créer et activer l’environnement

Avec Conda :

```bash
conda create -n rag-juridique python=3.10
conda activate rag-juridique
```

Ou avec venv :

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 4. 📚 Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. 🔑 Configurer les variables d’environnement

Crée un fichier `.env` à la racine du projet :

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

⚠️ **Ne jamais pousser ce fichier sur GitHub** (il est ignoré via `.gitignore`).

---

## ▶️ Utilisation de l'API

### 1. Démarrer le serveur

```bash
python app.py
```

Le serveur démarrera sur `http://0.0.0.0:5000`.

### 2. Lancer une requête

Vous pouvez interroger l'API en utilisant un client HTTP comme `curl`.

```bash
curl -X POST http://127.0.0.1:5000/query \
-H "Content-Type: application/json" \
-d '{"question": "Quels sont les droits du salarié selon le Code du travail camerounais ?"}'
```

### 3. Exemple de sortie

```json
{
  "answer": "Le salarié bénéficie du droit à un contrat écrit, à une rémunération équitable, à des congés annuels et à la protection sociale conformément au Code du travail.",
  "sources": [
    {
      "content": "...",
      "metadata": {
        "source": "...",
        "page": "..."
      }
    }
  ]
}
```

---

## 📁 Structure du projet

```
axe5/
├── app.py              # Point d’entrée de l'API
├── rag_juridique_mistral.py # Logique du système RAG
├── requirements.txt    # Dépendances Python
├── .env                # Variables locales (non versionné)
├── .gitignore
└── README.md
```

---

## 🛡️ Notes

- Les clés API doivent rester locales et privées.
- Le système est conçu pour être extensible (ajout de nouvelles sources, modèles, etc.).
```

---
