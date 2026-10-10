# LLM_Local — Laboratoire d’expérimentation LLM & RAG

## Présentation

**LLM_Local** est un projet personnel d’expérimentation dont l’objectif est d’apprendre par la pratique en implémentant, étape par étape, les méthodes et les briques logicielles qui constituent les assistants IA modernes.

Plutôt que de s’appuyer sur des frameworks de haut niveau qui masquent une partie de la complexité, le projet vise à comprendre **comment ces systèmes fonctionnent à l'interierieur**.

## Chronologie du projet

Le développement suit une progression itérative, au rythme des apprentissages et des expérimentations.

### Phase 1 — Fondations et API

- **Découverte du backend :** première expérience de création d’une API, avec l’apprentissage de l’architecture backend, du traitement des requêtes et de la structuration des endpoints avec FastAPI et `routes.py`.
- **Mécanique des LLM :** reproduction de composants présents dans les assistants conversationnels, notamment la gestion de l’historique, le streaming des tokens et la construction d’une interface de chat.
- **Prompts système et Ollama :** découverte de l’inférence locale avec Ollama et expérimentation avec les instructions système pour guider le comportement du modèle.
- **Tokenisation :** approfondissement et mise en pratique des connaissances sur la tokenisation des textes.

### Phase 2 — Moteur RAG « from scratch »

- **Implémentation du RAG :** construction manuelle des différentes étapes du processus, sans LangChain ni LlamaIndex, afin d’en comprendre les mécanismes.
- **Vectorisation et chunking :** création de stratégies de découpage avec `FixedChunker` et `HierarchicalChunker`, selon une architecture parent-enfant.
- **Mesure de similarité :** implémentation de méthodes de recherche vectorielle par similarité cosinus, produit scalaire et approche hybride.
- **Persistance :** utilisation de SQLite comme base de données relationnelle et vectorielle pour stocker les embeddings et l’historique des conversations.

## Architecture

Le projet suit une architecture modulaire qui sépare les responsabilités entre l’API, les services, le moteur RAG, les loaders et la base de données.

```text
.
├── app
│   ├── api
│   │   ├── routes.py
│   │   ├── frontend.py
│   │   └── schemas.py
│   ├── core
│   │   └── container.py
│   ├── database
│   │   ├── sqlite.py
│   │   └── schema.sql
│   ├── llm
│   │   ├── ollama_client.py
│   │   └── prompts/
│   │       └── system.py
│   ├── models
│   │   ├── conversation.py
│   │   └── message.py
│   ├── rag
│   │   ├── chunkers
│   │   │   ├── fixed_chunker.py
│   │   │   └── hierarchical_chunker.py
│   │   ├── embeddings
│   │   │   └── ollama_embeddings.py
│   │   ├── loaders
│   │   │   ├── text_loader.py
│   │   │   ├── pdf_loader.py
│   │   │   └── markdown_loader.py
│   │   ├── retrievers
│   │   │   └── vector_retriever.py
│   │   ├── services
│   │   │   └── document_indexer.py
│   │   ├── similarity
│   │   │   ├── cosine_similarity.py
│   │   │   └── hybride_similarity.py
│   │   └── vectorstores
│   │       └── sqlite_vector_store.py
│   ├── repositories
│   │   └── sqlite_repository.py
│   ├── services
│   │   └── chat_service_with_retriever.py
│   └── static
│       ├── app.js
│       ├── index.html
│       └── style.css
├── data
├── tests
└── main.py
```

## Technologies utilisées

- **Python 3.11 / 3.12**
- **FastAPI et Uvicorn** — serveur API
- **Ollama** — inférence locale et modèles d’embeddings, comme `nomic-embed-text`
- **SQLite** — stockage relationnel et vectoriel
- **Pytest** — tests unitaires et d’intégration
- **HTML, CSS et JavaScript vanilla** — interface interactive avec streaming SSE

## Installation et lancement

### 1. Cloner le projet et préparer l’environnement

Remplacez l’URL ci-dessous par celle de votre dépôt :

```bash
git clone [https://github.com/votre-utilisateur/llm_local.git](https://github.com/votre-utilisateur/llm_local.git)
cd llm_local

python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows, activez l’environnement avec :

```powershell
.venv\Scripts\activate
```

Installez ensuite les dépendances :

```bash
pip install -r requirements.txt
```

### 2. Configurer Ollama

Installez [Ollama](https://ollama.com/), puis récupérez les modèles nécessaires :

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

`mistral` est le modèle de langage utilisé par défaut. `nomic-embed-text` sert à générer les embeddings nécessaires au RAG.

### 3. Lancer l’application

```bash
uvicorn app.main:app --reload
```

L’interface de chat est accessible à l’adresse [http://localhost:8000/docs/index.html](http://localhost:8000/docs/index.html), selon la configuration de montage des fichiers statiques.

## Fonctionnement de l’application

- **Chat interactif :** l’utilisateur converse avec un LLM exécuté localement. Les réponses sont diffusées en temps réel.
- **Ingestion de documents :** un document PDF, Markdown (`.md`) ou texte (`.txt`) peut être ajouté directement depuis l’interface.
- **Traitement des documents :** le document est lu, découpé en chunks hiérarchiques, vectorisé, puis enregistré de manière persistante dans SQLite.
- **Génération augmentée :** lors des questions suivantes, le système recherche les passages pertinents dans SQLite et les ajoute au contexte transmis au LLM pour produire une réponse.

## Tests

Les tests automatisés couvrent le moteur RAG et l’API. Pour les lancer :

```bash
pytest
```

## Prochaines étapes — Phase 3

La prochaine phase portera sur l’**IA agentique** : permettre au LLM de décider quand utiliser des fonctions externes, comme un calculateur, et d’en exploiter les résultats de façon autonome.