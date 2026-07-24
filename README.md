# LLM_Perso

## Présentation

**LLM_Perso** est un projet personnel de création d’un assistant conversationnel privé basé sur un Large Language Model (LLM) exécuté localement.

Ce projet a avant tout une visée d’apprentissage : il me permet de comprendre concrètement comment fonctionnent les différents éléments d’une architecture RAG (Retrieval-Augmented Generation), de l’ingestion de documents jusqu’à la génération de réponses contextualisées.

Il me sert également de support pratique pour me familiariser avec **Git** et adopter de bonnes habitudes de versionnement tout au long du développement.

L’objectif est de disposer d’une API capable de :

- importer des documents ;
- les découper en segments (*chunks*) ;
- générer leurs embeddings ;
- les indexer dans une base vectorielle ;
- retrouver les passages les plus pertinents lors d’une question ;
- générer une réponse contextualisée grâce à un LLM local.

## Objectifs du projet

Les principaux objectifs sont :

- comprendre le rôle et le fonctionnement des différentes briques d’une architecture RAG ;
- développer un assistant IA fonctionnant entièrement en local ;
- garantir la confidentialité des données ;
- apprendre à concevoir une API REST avec FastAPI ;
- utiliser des modèles d’embeddings pour la recherche sémantique ;
- construire une base de code modulaire et facilement extensible ;
- se familiariser avec Git et les bonnes pratiques de gestion de versions.

## Architecture

Le projet est organisé selon une architecture modulaire :

```text
.
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── config.cpython-312.pyc
│   │   ├── main.cpython-312.pyc
│   │   └── memory.cpython-312.pyc
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312 2.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── frontend.cpython-312 2.pyc
│   │   │   ├── frontend.cpython-312.pyc
│   │   │   ├── routes.cpython-312 2.pyc
│   │   │   ├── routes.cpython-312.pyc
│   │   │   └── schemas.cpython-312.pyc
│   │   ├── frontend.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── config.py
│   ├── database
│   │   ├── __init__ 2.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── database.cpython-312.pyc
│   │   ├── database.py
│   │   ├── schema 2.sql
│   │   ├── schema.sql
│   │   ├── sqlite 2.py
│   │   └── sqlite.py
│   ├── llm
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312 2.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── client.cpython-312 2.pyc
│   │   │   ├── client.cpython-312.pyc
│   │   │   ├── llm.cpython-312 2.pyc
│   │   │   ├── llm.cpython-312.pyc
│   │   │   ├── ollama_client.cpython-312.pyc
│   │   │   ├── prompts.cpython-312 2.pyc
│   │   │   └── prompts.cpython-312.pyc
│   │   ├── client.py
│   │   ├── ollama_client.py
│   │   └── prompts
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   └── system.cpython-312.pyc
│   │       └── system.py
│   ├── main.py
│   ├── models
│   │   ├── __pycache__
│   │   │   ├── conversation.cpython-312.pyc
│   │   │   └── message.cpython-312.pyc
│   │   ├── __pycache__ 2
│   │   ├── conversation 2.py
│   │   ├── conversation.py
│   │   ├── message 2.py
│   │   └── message.py
│   ├── monitoring
│   │   ├── __pycache__
│   │   │   └── generation_metrics.cpython-312.pyc
│   │   └── generation_metrics.py
│   ├── rag
│   │   ├── chunkers
│   │   │   ├── __pycache__
│   │   │   │   ├── chunker.cpython-311.pyc
│   │   │   │   └── fixed_chunker.cpython-311.pyc
│   │   │   ├── __pycache__ 2
│   │   │   ├── chunker.py
│   │   │   └── fixed_chunker.py
│   │   ├── embeddings
│   │   │   ├── __pycache__
│   │   │   │   ├── embedding.cpython-312.pyc
│   │   │   │   ├── embedding.cpython-313.pyc
│   │   │   │   ├── ollama_embeddings.cpython-312.pyc
│   │   │   │   └── ollama_embeddings.cpython-313.pyc
│   │   │   ├── __pycache__ 2
│   │   │   ├── embedding.py
│   │   │   └── ollama_embeddings.py
│   │   ├── loaders
│   │   │   ├── document_loader.py
│   │   │   └── text_loader.py
│   │   ├── models
│   │   │   ├── __pycache__
│   │   │   │   ├── chunk.cpython-311.pyc
│   │   │   │   └── document.cpython-311.pyc
│   │   │   ├── __pycache__ 2
│   │   │   ├── chunk.py
│   │   │   └── document.py
│   │   ├── retrievers
│   │   ├── services
│   │   │   ├── __pycache__
│   │   │   │   └── document_indexer.cpython-311.pyc
│   │   │   ├── __pycache__ 2
│   │   │   ├── document_indexer.py
│   │   │   └── document_service.py
│   │   ├── similarity
│   │   │   ├── __pycache__
│   │   │   │   ├── cosine_similarity.cpython-311.pyc
│   │   │   │   └── similarity.cpython-311.pyc
│   │   │   ├── __pycache__ 2
│   │   │   ├── cosine_similarity.py
│   │   │   └── similarity.py
│   │   └── vectorstores
│   │       ├── __pycache__
│   │       │   ├── memory_vector_store.cpython-311.pyc
│   │       │   └── vector_store.cpython-311.pyc
│   │       ├── __pycache__ 2
│   │       ├── memory_vector_store.py
│   │       └── vector_store.py
│   ├── repositories
│   │   ├── __init__ 2.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── conversation_repository.cpython-312.pyc
│   │   │   ├── memory_repository.cpython-312.pyc
│   │   │   └── sqlite_repository.cpython-312.pyc
│   │   ├── __pycache__ 2
│   │   ├── conversation_repository 2.py
│   │   ├── conversation_repository.py
│   │   ├── memory_repository 2.py
│   │   ├── memory_repository.py
│   │   ├── sqlite_repository 2.py
│   │   └── sqlite_repository.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312 2.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── chat_service.cpython-312 2.pyc
│   │   │   ├── chat_service.cpython-312.pyc
│   │   │   ├── conversation_service.cpython-312 2.pyc
│   │   │   └── conversation_service.cpython-312.pyc
│   │   ├── chat_service.py
│   │   └── conversation_service.py
│   ├── static
│   │   ├── app.js
│   │   ├── index_original.html
│   │   ├── index.html
│   │   └── style.css
│   └── tokenizers
│       ├── __pycache__
│       │   ├── simple_tokenizer.cpython-312.pyc
│       │   └── tokenizer.cpython-312.pyc
│       ├── llama_cpp_tokenizer.py
│       ├── simple_tokenizer.py
│       ├── tiktoken_tokenizer.py
│       ├── tokenizer.py
│       └── transformers_tokenizer.py
├── ARCHITECTURE.md
├── CHANGELOG.md
├── data
│   ├── assistant 2.db
│   └── assistant.db
├── pytest.ini
├── README.md
├── requirements.txt
├── ROADMAP.md
└── tests
    ├── __pycache__
    │   ├── test_document_indexer.cpython-311-pytest-8.3.3.pyc
    │   ├── test_fixed_chunker.cpython-311-pytest-8.3.3.pyc
    │   └── test_memory_vector_store.cpython-311-pytest-8.3.3.pyc
    ├── __pycache__ 2
    ├── fake_class
    │   ├── __pycache__
    │   │   ├── fake_embedding.cpython-311.pyc
    │   │   └── fake_vectore_store.cpython-311.pyc
    │   ├── fake_embedding.py
    │   └── fake_vectore_store.py
    ├── fake_class 2
    ├── test_document_indexer.py
    ├── test_fixed_chunker.py
    └── test_memory_vector_store.py
```

Chaque module possède une responsabilité unique afin de faciliter la maintenance et l’évolution du projet.

## Technologies utilisées

Le projet repose principalement sur les technologies suivantes :

- Python 3.12
- FastAPI
- Uvicorn
- Ollama
- ChromaDB
- SentenceTransformers
- Pytest
- Pydantic

## Fonctionnement général

Le fonctionnement du projet se déroule selon les étapes suivantes :

1. Un document est importé.
2. Le document est chargé en mémoire.
3. Son contenu est découpé en plusieurs morceaux (*chunks*).
4. Un embedding est généré pour chaque chunk.
5. Les embeddings sont enregistrés dans ChromaDB.
6. L’utilisateur pose une question.
7. Une recherche vectorielle retrouve les passages les plus pertinents.
8. Ces passages sont ajoutés au prompt envoyé au LLM.
9. Le modèle génère une réponse basée sur le contexte retrouvé.

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/llm_perso.git
cd llm_perso
```

### 2. Créer un environnement virtuel

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Installer Ollama

Télécharger Ollama puis récupérer un modèle compatible.

Exemple :

```bash
ollama pull mistral
```

ou

```bash
ollama pull llama3
```

### 5. Lancer l’API

```bash
uvicorn app.main:app --reload
```

L’API sera disponible à l’adresse suivante :

[http://localhost:8000](http://localhost:8000)

La documentation interactive sera accessible via :

[http://localhost:8000/docs](http://localhost:8000/docs)

## Ingestion des documents

L’API permet d’importer un document qui sera automatiquement :

- chargé ;
- découpé ;
- vectorisé ;
- indexé dans ChromaDB.

Cette étape prépare les données afin qu’elles puissent être utilisées lors des futures recherches.

## Recherche sémantique

Lorsqu’une question est posée :

- la question est convertie en embedding ;
- une recherche par similarité est effectuée ;
- les passages les plus pertinents sont récupérés.

Cette approche permet de retrouver des informations même lorsque les mots utilisés diffèrent de ceux présents dans le document.

## Génération des réponses

Les passages retrouvés sont injectés dans le prompt du modèle.

Le LLM utilise alors :

- la question de l’utilisateur ;
- le contexte retrouvé ;
- ses connaissances générales.

La réponse produite est ainsi plus précise et mieux adaptée aux documents indexés.

## Tests

Les tests unitaires sont réalisés avec Pytest.

Exécution :

```bash
pytest
```

Les tests permettent notamment de vérifier :

- le chargement des documents ;
- le découpage en chunks ;
- la génération des embeddings ;
- les services d’ingestion ;
- le fonctionnement global des composants.

## Évolutions prévues

Les améliorations envisagées sont les suivantes :

- prise en charge des PDF ;
- prise en charge des fichiers Word ;
- historique des conversations ;
- gestion de plusieurs collections ChromaDB ;
- authentification des utilisateurs ;
- interface web ;
- streaming des réponses ;
- mémoire conversationnelle ;
- support de plusieurs modèles LLM.

## Bonnes pratiques

Le projet suit plusieurs principes de développement :

- architecture en couches ;
- séparation des responsabilités ;
- code typé avec Python ;
- tests unitaires ;
- services indépendants ;
- documentation de l’API avec OpenAPI.

## Auteur

Projet développé dans une démarche d’apprentissage pour mieux comprendre les architectures RAG, le fonctionnement des modèles de langage en local, ainsi que l’utilisation de Git dans un cadre de développement progressif.

## Licence

Ce projet est distribué sous licence MIT. Vous êtes libre de le modifier, de l’utiliser et de le partager conformément aux termes de cette licence.
