
# Projet `llm_local` — Contexte de reprise

## 1. Vision du projet

Le projet est un assistant personnel local développé en Python.

L'objectif initial était de construire un assistant conversationnel utilisant un LLM local avec :

- Ollama pour l'inférence ;
- FastAPI pour l'API ;
- SQLite pour la persistance ;
- un système RAG développé progressivement "from scratch" ;
- pytest pour les tests ;
- une architecture organisée en services, repositories et abstractions.

La vision a progressivement évolué.

Le projet doit maintenant devenir à terme un **assistant personnel agentique local**, capable non seulement de discuter et de rechercher dans des documents, mais également :

- d'utiliser des outils ;
- de prendre des décisions simples ;
- d'enchaîner plusieurs actions ;
- d'effectuer des automatisations ;
- de conserver une mémoire/connaissance personnalisée ;
- éventuellement de gérer plusieurs utilisateurs ;
- de fonctionner avec plusieurs modèles/providers.

L'objectif important est de **comprendre et construire soi-même les mécanismes d'Agentic AI**, plutôt que de simplement utiliser un framework existant.

OpenClaw est utilisé comme **source d'inspiration et de comparaison**, mais l'objectif est de faire évoluer `llm_local` progressivement pour comprendre les mécanismes sous-jacents.

---

# 2. Architecture actuelle

Structure logique actuelle :

```text
.
├── app
│   ├── __init__.py
│   │
│   ├── api
│   │   ├── __init__.py
│   │   ├── documents.py
│   │   ├── frontend.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── config.py
│   │
│   ├── core
│   │   └── container.py
│   │
│   ├── database
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── schema.sql
│   │   └── sqlite.py
│   │
│   ├── llm
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── ollama_client.py
│   │   └── prompts
│   │       ├── __init__.py
│   │       └── system.py
│   │
│   ├── main.py
│   │
│   ├── models
│   │   ├── conversation.py
│   │   └── message.py
│   │
│   ├── monitoring
│   │   └── generation_metrics.py
│   │
│   ├── rag
│   │   ├── chunkers
│   │   │   ├── chunker.py
│   │   │   └── fixed_chunker.py
│   │   │
│   │   ├── embeddings
│   │   │   ├── embedding.py
│   │   │   └── ollama_embeddings.py
│   │   │
│   │   ├── loaders
│   │   │   ├── document_loader.py
│   │   │   └── text_loader.py
│   │   │
│   │   ├── models
│   │   │   ├── chunk.py
│   │   │   ├── document.py
│   │   │   └── search_results.py
│   │   │
│   │   ├── retrievers
│   │   │   ├── retriever.py
│   │   │   └── vector_retriever.py
│   │   │
│   │   ├── services
│   │   │   ├── document_indexer.py
│   │   │   └── document_service.py
│   │   │
│   │   ├── similarity
│   │   │   ├── cosine_similarity.py
│   │   │   └── similarity.py
│   │   │
│   │   └── vectorstores
│   │       ├── memory_vector_store.py
│   │       └── vector_store.py
│   │
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── conversation_repository.py
│   │   ├── memory_repository.py
│   │   └── sqlite_repository.py
│   │
│   ├── services
│   │   ├── __init__.py
│   │   ├── chat_service_with_retriever.py
│   │   ├── chat_service.py
│   │   └── conversation_service.py
│   │
│   ├── static
│   │   ├── app.js
│   │   ├── index_original.html
│   │   ├── index.html
│   │   └── style.css
│   │
│   └── tokenizers
│       ├── llama_cpp_tokenizer.py
│       ├── simple_tokenizer.py
│       ├── tiktoken_tokenizer.py
│       ├── tokenizer.py
│       └── transformers_tokenizer.py
│
├── ARCHITECTURE.md
├── CHANGELOG.md
├── README.md
├── ROADMAP.md
├── pytest.ini
├── requirements.txt
│
├── data
│   ├── assistant.db
│   └── assistant 2.db
│
└── tests
    ├── fake_class
    │   ├── fake_embedding.py
    │   └── fake_vectore_store.py
    │
    └── rag
        ├── test_document_indexer.py
        ├── test_embedding.py
        ├── test_fixed_chunker.py
        ├── test_memory_vector_store.py
        └── test_vector_retriever.py
```

Les `__pycache__` ne sont pas considérés comme faisant partie de la structure fonctionnelle.

---

# 3. Choix techniques

## Langage

Python.

Raisons :

- écosystème IA très important ;
- intégration naturelle avec les LLM ;
- FastAPI ;
- pytest ;
- possibilité d'évoluer vers des composants agentiques et automatisés.

---

## LLM

Le LLM est exécuté localement via **Ollama**.

L'application ne dépend pas directement d'Ollama partout.

Une abstraction a été créée :

```text
app/llm/client.py
```

et l'implémentation actuelle :

```text
app/llm/ollama_client.py
```

L'idée est :

```text
ChatService
     ↓
LLMClient
     ↓
OllamaClient
     ↓
Ollama
     ↓
Modèle local
```

Ainsi, le service métier ne doit pas être fortement couplé à Ollama.

À terme, il doit être possible d'ajouter un autre provider/modèle sans réécrire toute l'application.

---

# 4. Ollama et environnement

Le développement est effectué sur un MacBook Pro équipé d'une puce Apple M3 Pro.

Il existe deux comptes macOS :

```text
axellantin
jeux
```

L'objectif est d'utiliser le compte `jeux` pour l'environnement de travail.

Ollama a été testé sous `jeux`.

Résultat important :

```text
OLLAMA_MODELS:/Users/jeux/.ollama/models
OLLAMA_HOST:http://127.0.0.1:11434
Listening on 127.0.0.1:11434
```

Ollama détecte correctement le GPU Metal :

```text
Apple M3 Pro
```

avec environ :

```text
13.3 GiB VRAM disponible
```

Les modèles visibles sous `jeux` comprennent notamment :

```text
qwen2:1.5b
phi3:latest
llama3:latest
nomic-embed-text:latest
mistral:latest
```

Attention : le test qui reste à faire est de laisser :

```bash
ollama serve
```

tourner dans un terminal sous `jeux`, puis dans un second terminal :

```bash
ollama run qwen2:1.5b
```

Le `Ctrl+C` envoyé au premier terminal arrête le serveur et provoque naturellement :

```text
could not connect to ollama server
```

Donc ce comportement n'est pas une erreur Ollama.

---

# 5. Persistance des conversations

Les conversations sont représentées par :

```python
@dataclass
class Conversation:
    id: str
    messages: list[Message]
    title: str
```

Chaque conversation possède un UUID.

Les messages sont représentés par `Message`.

SQLite est utilisé pour persister :

```text
conversations
messages
```

Schéma actuel :

```sql
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY(conversation_id)
        REFERENCES conversations(id)
);
```

Le repository utilisé est :

```text
app/repositories/sqlite_repository.py
```

L'architecture suit l'idée :

```text
Service
  ↓
Repository
  ↓
SQLite
```

Cela permet de changer ultérieurement le mécanisme de persistance sans modifier toute la logique métier.

---

# 6. ChatService

Le service principal actuel gère notamment :

- récupération de conversation ;
- ajout du message utilisateur ;
- construction des messages ;
- appel au LLM ;
- streaming de la réponse ;
- calcul des métriques ;
- sauvegarde de la réponse assistant.

Le prompt système est séparé dans :

```text
app/llm/prompts/system.py
```

L'objectif est de ne pas mélanger les prompts avec la logique métier.

---

# 7. Monitoring

Un composant existe :

```text
app/monitoring/generation_metrics.py
```

Il mesure notamment :

- nombre de messages ;
- caractères en entrée ;
- caractères en sortie ;
- tokens en entrée ;
- tokens en sortie ;
- temps de génération ;
- tokens/seconde ;
- timestamp.

L'idée est de commencer simplement avec ces métriques puis de construire plus tard un dashboard.

Il existe actuellement une petite incohérence dans `GenerationMetrics` :

- les champs `model` et `provider` sont déclarés ;
- le constructeur actuel ne les initialise pas ;
- `timestamp` est déclaré comme `datetime` mais reçoit actuellement un timestamp numérique.

Ce point devra être nettoyé lors d'un futur refactoring.

---

# 8. Tokenizers

Le projet possède plusieurs abstractions/implémentations :

```text
app/tokenizers/
├── llama_cpp_tokenizer.py
├── simple_tokenizer.py
├── tiktoken_tokenizer.py
├── tokenizer.py
└── transformers_tokenizer.py
```

L'objectif est de garder la possibilité de changer la méthode de comptage des tokens.

Cela est particulièrement intéressant pour :

- mesurer les coûts/performances ;
- gérer les fenêtres de contexte ;
- contrôler la taille du RAG ;
- construire plus tard un système de mémoire intelligent.

---

# 9. RAG

Le RAG est développé volontairement "from scratch".

L'objectif pédagogique est de comprendre chaque étape plutôt que de brancher directement une solution complète.

Architecture :

```text
Document
   ↓
Loader
   ↓
Chunker
   ↓
Embedding
   ↓
Vector Store
   ↓
Retriever
   ↓
Context
   ↓
LLM
```

---

# 10. Documents

Les documents sont représentés dans :

```text
app/rag/models/document.py
```

Les morceaux de documents sont représentés dans :

```text
app/rag/models/chunk.py
```

Un document peut donc être transformé en plusieurs chunks.

---

# 11. Loaders

Architecture :

```text
app/rag/loaders/
├── document_loader.py
└── text_loader.py
```

Le loader texte existe déjà.

L'objectif futur est d'ajouter notamment :

```text
.txt
.md
.pdf
.docx
```

sans modifier le reste du pipeline.

---

# 12. Chunking

Architecture :

```text
app/rag/chunkers/
├── chunker.py
└── fixed_chunker.py
```

Le `FixedChunker` permet actuellement de découper un document en chunks de taille fixe.

Une abstraction `Chunker` existe afin de pouvoir expérimenter ensuite avec :

- taille fixe ;
- overlap ;
- découpage par paragraphes ;
- découpage sémantique ;
- éventuellement stratégies spécifiques au type de document.

---

# 13. Embeddings

Architecture :

```text
app/rag/embeddings/
├── embedding.py
└── ollama_embeddings.py
```

L'interface d'embedding est séparée de son implémentation.

L'implémentation actuelle utilise Ollama.

Un modèle de type embedding local est disponible :

```text
nomic-embed-text
```

Les embeddings servent à représenter les chunks sous forme de vecteurs.

---

# 14. Similarité

Architecture :

```text
app/rag/similarity/
├── similarity.py
└── cosine_similarity.py
```

La similarité cosinus est utilisée pour comparer :

```text
embedding de la question
        ↓
embedding des chunks
```

et déterminer quels chunks sont les plus proches.

---

# 15. Vector Store

Architecture :

```text
app/rag/vectorstores/
├── vector_store.py
└── memory_vector_store.py
```

Le `MemoryVectorStore` conserve actuellement les chunks et embeddings en mémoire.

La recherche fait essentiellement :

```text
embedding question
        ↓
comparaison avec tous les chunks
        ↓
score cosine
        ↓
tri décroissant
        ↓
top K
```

La recherche actuelle ressemble conceptuellement à :

```python
scores = []

for chunk in self.chunks:
    score = self.similarity.score(
        embedding,
        chunk.embedding
    )

    scores.append((score, chunk))

scores.sort(
    reverse=True,
    key=lambda item: item[0]
)

return [chunk for _, chunk in scores[:k]]
```

C'est volontairement simple pour comprendre le fonctionnement.

Plus tard, le vector store devra devenir persistant et plus performant.

---

# 16. Retriever

Architecture :

```text
app/rag/retrievers/
├── retriever.py
└── vector_retriever.py
```

Le retriever fait le lien entre :

```text
question
    ↓
embedding
    ↓
vector store
    ↓
résultats pertinents
```

Les résultats sont représentés avec :

```text
app/rag/models/search_results.py
```

Le retriever est donc une abstraction importante pour la suite.

---

# 17. Indexation

Architecture :

```text
app/rag/services/
├── document_indexer.py
└── document_service.py
```

Le `DocumentIndexer` orchestre notamment :

```text
Document
 ↓
Chunks
 ↓
Embeddings
 ↓
VectorStore
```

Les tests unitaires de cette partie sont déjà présents.

---

# 18. Tests RAG

Les tests actuels :

```text
tests/rag/
├── test_document_indexer.py
├── test_embedding.py
├── test_fixed_chunker.py
├── test_memory_vector_store.py
└── test_vector_retriever.py
```

Des classes fake existent également :

```text
tests/fake_class/
├── fake_embedding.py
└── fake_vectore_store.py
```

Tous les tests RAG existants passent actuellement.

C'est important : les briques individuelles sont donc déjà validées.

---

# 19. Ce qui manque actuellement au RAG

Le principal travail immédiat consiste maintenant à faire fonctionner le **RAG de bout en bout**.

Il faut assembler :

```text
Document
 ↓
TextLoader
 ↓
FixedChunker
 ↓
Embedding
 ↓
MemoryVectorStore
 ↓
VectorRetriever
 ↓
contexte
 ↓
ChatServiceWithRetriever
 ↓
LLM
 ↓
réponse
```

Le fichier important pour cette étape est :

```text
app/services/chat_service_with_retriever.py
```

Il faut vérifier son implémentation actuelle avant de modifier l'architecture.

---

# 20. Premier test RAG end-to-end

Le premier test doit être volontairement simple.

Créer un petit document fictif :

```text
Le projet llm_local est un assistant personnel local.
Il utilise Ollama pour exécuter un modèle de langage.
Le système possède également un moteur RAG.
```

Puis poser une question :

```text
Quel système est utilisé pour exécuter le modèle de langage ?
```

Le pipeline doit :

```text
document
 ↓
chunk
 ↓
embedding
 ↓
index
 ↓
retrieval
 ↓
contexte
 ↓
LLM
 ↓
"Le projet utilise Ollama."
```

Le but est d'abord de vérifier le fonctionnement, pas encore d'optimiser la qualité.

---

# 21. Sources dans les réponses

Une évolution importante du RAG sera de ne pas simplement retourner :

```text
réponse
```

mais quelque chose comme :

```text
réponse

Sources :
- document.txt
- document.txt, chunk 3
```

Le système doit conserver suffisamment de metadata pour savoir d'où provient chaque chunk.

C'est particulièrement important pour un assistant personnel.

---

# 22. Persistance du RAG

Actuellement :

```text
MemoryVectorStore
```

signifie que l'index disparaît lorsque l'application redémarre.

Il faudra donc ensuite créer un vector store persistant.

Objectif :

```text
documents
     ↓
embeddings
     ↓
vector database
     ↓
redémarrage
     ↓
index toujours disponible
```

Il n'est pas nécessaire de choisir immédiatement une grosse solution.

L'objectif pédagogique est d'abord de bien comprendre l'abstraction :

```text
VectorStore
```

puis de remplacer l'implémentation.

---

# 23. Métadonnées

Le système devra ensuite enrichir les chunks avec des métadonnées telles que :

```text
document_id
filename
source
chunk_id
user_id
created_at
```

Cela permettra notamment de faire :

```text
question
   ↓
filtrage user_id
   ↓
recherche vectorielle
   ↓
top K
```

C'est essentiel pour éviter qu'un utilisateur puisse récupérer les données d'un autre.

---

# 24. Multi-utilisateur

Une évolution prévue est d'ajouter une authentification.

Architecture cible :

```text
Utilisateur
    ↓
Authentification
    ↓
user_id
    ↓
Conversation
    ↓
RAG filtré par user_id
```

La base devra donc évoluer pour associer les ressources à un utilisateur.

---

# 25. RAG personnalisé

À terme, le système doit pouvoir avoir une connaissance spécifique à chaque utilisateur.

Exemple :

```text
Utilisateur A
 ├── documents personnels
 ├── conversations
 └── mémoire

Utilisateur B
 ├── documents personnels
 ├── conversations
 └── mémoire
```

Le RAG devra respecter cette séparation.

---

# 26. Architecture Agentic AI cible

Une fois le RAG stabilisé, le projet évoluera vers une architecture agentique.

Conceptuellement :

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                ↓
                         ┌──────────────┐
                         │    Agent     │
                         │              │
                         │ LLM + Memory │
                         │    + Tools   │
                         └──────┬───────┘
                                ↓
                         Décision / Plan
                                ↓
                    ┌───────────┴───────────┐
                    ↓                       ↓
                  Tool                    RAG
                    ↓                       ↓
                 Result                  Context
                    └───────────┬───────────┘
                                ↓
                               LLM
                                ↓
                    ┌───────────┴───────────┐
                    ↓                       ↓
              réponse finale           autre outil
```

L'idée fondamentale est que le LLM ne sert plus seulement à répondre.

Il devient capable de décider :

```text
"Je peux répondre directement"
```

ou :

```text
"J'ai besoin du RAG"
```

ou :

```text
"Je dois utiliser la calculatrice"
```

ou :

```text
"Je dois utiliser un autre outil"
```

---

# 27. Première étape Agentic AI

La première tool doit être volontairement très simple.

Exemple :

```text
calculator
```

Question :

```text
Combien font 145 * 37 ?
```

Le LLM doit pouvoir décider :

```text
tool = calculator
input = 145 * 37
```

Le programme exécute réellement :

```text
calculator
```

puis retourne :

```text
5365
```

au LLM.

Le LLM peut alors construire la réponse finale.

Cela permet de comprendre concrètement la boucle agentique.

---

# 28. Architecture Agent envisagée

Une structure possible :

```text
app/
├── agent/
│   ├── agent.py
│   ├── planner.py
│   ├── tool_registry.py
│   └── tool_executor.py
│
└── tools/
    ├── calculator.py
    ├── filesystem.py
    ├── web.py
    └── ...
```

Mais **ne pas créer toute cette architecture immédiatement**.

Elle doit apparaître progressivement lorsque le premier outil sera nécessaire.

---

# 29. Principe important pour les Tools

Il ne faut pas donner immédiatement au LLM un accès arbitraire au système.

À éviter au début :

```text
LLM → shell arbitraire → machine
```

Préférer :

```text
LLM
 ↓
outil explicitement enregistré
 ↓
validation
 ↓
exécution
 ↓
résultat
```

Pour les outils ayant des effets réels, une validation utilisateur pourra être nécessaire.

Exemple :

```text
Agent :
"Je peux envoyer cet email. Voulez-vous confirmer ?"

Utilisateur :
"Oui"

Agent :
→ exécution
```

---

# 30. Automatisations

Une fois le mécanisme d'agent compris, le projet pourra évoluer vers des automatisations.

Exemples possibles :

```text
Tous les matins à 8h
    ↓
Agent
    ↓
récupérer certaines informations
    ↓
RAG
    ↓
générer résumé
    ↓
envoyer notification
```

Ou :

```text
Chaque lundi
    ↓
scanner certains documents
    ↓
indexer les nouveaux fichiers
    ↓
mettre à jour le RAG
```

Ou :

```text
condition
    ↓
Agent
    ↓
outil
    ↓
action
```

Cela nécessitera ensuite un scheduler/gestionnaire de tâches.

---

# 31. Vision finale

La vision cible du projet est :

```text
                    ┌───────────────────┐
                    │       User        │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │      Agent        │
                    │                   │
                    │       LLM         │
                    │     Planner       │
                    │      Memory       │
                    └───────┬───────────┘
                            ↓
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
             RAG          Tools       Automations
              ↓             ↓             ↓
         Documents      Calculator     Scheduler
         Knowledge      Filesystem      Jobs
         Memory         Web             Actions
              └─────────────┼─────────────┘
                            ↓
                         Result
                            ↓
                           LLM
                            ↓
                     Final response
```

---

# 32. Roadmap globale

## Phase 1 — Assistant local

État : quasiment terminé.

```text
[x] Python
[x] FastAPI
[x] Ollama
[x] Chat
[x] Streaming
[x] SQLite
[x] Conversations
[x] Repository
[x] System prompt
[x] Tokenisation
[x] Monitoring de base
```

---

## Phase 2 — RAG fondamental

État : composants terminés, intégration à terminer.

```text
[x] Document model
[x] Chunk model
[x] Loader abstraction
[x] Text loader
[x] Chunker abstraction
[x] Fixed chunker
[x] Embedding abstraction
[x] Ollama embeddings
[x] Similarity abstraction
[x] Cosine similarity
[x] VectorStore abstraction
[x] Memory vector store
[x] Retriever abstraction
[x] Vector retriever
[x] SearchResult
[x] DocumentIndexer
[x] Tests unitaires
[ ] Intégration end-to-end
[ ] RAG + ChatService
[ ] Test RAG complet
```

**C'est la prochaine étape immédiate.**

---

## Phase 3 — RAG robuste

Après le premier pipeline complet :

```text
[ ] Sources dans les réponses
[ ] Metadata sur les chunks
[ ] VectorStore persistant
[ ] Meilleure stratégie de chunking
[ ] Chunk overlap
[ ] PDF
[ ] Markdown
[ ] DOCX
[ ] Gestion des documents
[ ] Réindexation
[ ] Suppression d'un document
[ ] Tests end-to-end
```

---

## Phase 4 — Personnalisation

```text
[ ] user_id
[ ] Authentification
[ ] Utilisateurs
[ ] Conversations liées aux utilisateurs
[ ] Documents liés aux utilisateurs
[ ] Filtrage RAG par user_id
[ ] Mémoire personnalisée
```

---

## Phase 5 — Premier Agent

```text
[ ] Tool abstraction
[ ] Tool registry
[ ] Tool executor
[ ] Calculator
[ ] Détection du besoin d'outil
[ ] Exécution outil
[ ] Retour du résultat au LLM
[ ] Boucle agentique minimale
```

Objectif pédagogique :

```text
LLM
 ↓
décide
 ↓
tool
 ↓
résultat
 ↓
LLM
 ↓
réponse
```

---

## Phase 6 — Agent plus évolué

```text
[ ] Planner
[ ] Plusieurs tools
[ ] RAG comme outil
[ ] Filesystem tool
[ ] Web tool
[ ] Memory tool
[ ] Tool permissions
[ ] Validation utilisateur
[ ] Gestion des erreurs
[ ] Limite du nombre d'itérations
```

---

## Phase 7 — Automatisations

```text
[ ] Scheduler
[ ] Jobs
[ ] Tâches récurrentes
[ ] Déclencheurs
[ ] Conditions
[ ] Historique des exécutions
[ ] Gestion des erreurs
[ ] Notifications
```

---

## Phase 8 — Observabilité

```text
[ ] Metrics propres
[ ] Model/provider dans les metrics
[ ] Temps d'inférence
[ ] Tokens/sec
[ ] Nombre d'appels tools
[ ] Temps RAG
[ ] Nombre de chunks récupérés
[ ] Logs
[ ] Dashboard
```

---

## Phase 9 — Multi-modèle / multi-provider

Grâce aux abstractions déjà mises en place :

```text
LLMClient
   ├── OllamaClient
   ├── autre provider
   └── éventuellement API distante
```

Même principe pour :

```text
Embedding
VectorStore
Retriever
```

L'objectif est de conserver une architecture indépendante des implémentations.

---

# 33. Ordre recommandé maintenant

Il ne faut pas essayer de développer tout le roadmap en même temps.

L'ordre recommandé est :

```text
1. Valider définitivement Ollama sous `jeux`
             ↓
2. Finir le RAG end-to-end
             ↓
3. Écrire le test end-to-end
             ↓
4. Ajouter les sources
             ↓
5. Persister le VectorStore
             ↓
6. Ajouter metadata
             ↓
7. Ajouter différents types de documents
             ↓
8. Auth + user_id
             ↓
9. Premier Tool : calculator
             ↓
10. Première boucle Agent
             ↓
11. RAG comme Tool
             ↓
12. Autres Tools
             ↓
13. Automatisations
             ↓
14. Monitoring / Dashboard
             ↓
15. Multi-model / multi-provider
```

Il est toutefois possible de commencer le **premier Tool** relativement tôt après le RAG end-to-end afin de commencer à apprendre concrètement l'Agentic AI.

---

# 34. Principes de développement du projet

Plusieurs principes ont été retenus.

### Comprendre avant d'abstraire

Ne pas ajouter immédiatement LangChain, LlamaIndex ou un autre framework simplement parce qu'il existe.

Le projet doit permettre de comprendre :

```text
embedding
retrieval
RAG
tool calling
agent loop
planning
memory
automation
```

avant éventuellement d'utiliser des frameworks.

### Une abstraction = un intérêt concret

Les interfaces existent pour permettre de remplacer les implémentations :

```text
LLMClient
Embedding
Chunker
VectorStore
Retriever
Repository
```

Il ne faut pas multiplier les abstractions inutiles.

### Tester chaque brique

L'approche utilisée est proche de celle d'un projet Java/JUnit :

```text
petite fonctionnalité
 ↓
test
 ↓
validation
 ↓
fonctionnalité suivante
```

Pytest est utilisé pour cela.

### Construire verticalement

Pour les nouvelles fonctionnalités importantes, privilégier :

```text
fonctionnalité minimale complète
```

plutôt que :

```text
20 classes abstraites
+
aucun flux fonctionnel
```

Exemple pour l'Agent :

```text
calculator
 ↓
agent
 ↓
LLM
 ↓
résultat
```

avant de créer un système complet de planning.

---

# 35. OpenClaw

OpenClaw n'est pas le cœur du projet.

Il sert de référence pour réfléchir à :

- agents ;
- outils ;
- mémoire ;
- automatisations ;
- interactions avec l'environnement.

L'objectif est de pouvoir comprendre ce qu'un système comme OpenClaw réalise conceptuellement.

Le projet personnel doit donc évoluer progressivement vers :

```text
LLM local
        ↓
Assistant
        ↓
RAG
        ↓
Tools
        ↓
Agent
        ↓
Automations
        ↓
Personal Assistant
```

---

# 36. Prochaine tâche concrète

La prochaine session doit reprendre **directement au RAG end-to-end**.

Commencer par inspecter :

```text
app/services/chat_service_with_retriever.py
app/rag/retrievers/vector_retriever.py
app/rag/models/search_results.py
```

Puis construire le flux :

```text
Document
 ↓
Loader
 ↓
Chunker
 ↓
Embedding
 ↓
VectorStore
 ↓
Retriever
 ↓
Context
 ↓
ChatServiceWithRetriever
 ↓
Ollama
 ↓
Response
```

Enfin écrire un test :

```text
test_rag_end_to_end.py
```

avec un petit document connu et une question dont la réponse se trouve dans le document.

**Ne pas commencer les Tools ou l'Agent avant d'avoir ce flux RAG fonctionnel.**

Une fois ce test vert, le projet aura franchi une étape importante :

```text
Assistant conversationnel
          +
      RAG fonctionnel
          ↓
      base solide
          ↓
    premier Agent
```

---

# 37. État mental du projet

Le projet n'est plus simplement :

```text
"faire un chatbot local"
```

mais devient progressivement :

```text
Construire et comprendre un
assistant personnel local agentique
```

avec trois grandes couches :

```text
┌──────────────────────────────┐
│        INTERACTION           │
│       FastAPI / UI           │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        INTELLIGENCE           │
│ LLM / RAG / Memory / Agent   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│          ACTIONS              │
│ Tools / Automations / Jobs   │
└──────────────────────────────┘
```

Le RAG constitue actuellement le pont entre le simple chatbot et cette architecture agentique.