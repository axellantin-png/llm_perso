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

CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    document_title TEXT,
    content TEXT NOT NULL,
    embedding TEXT NOT NULL,         -- Stocké sous forme de chaîne JSON (ex: "[0.12, -0.43, ...]")
    parent_content TEXT
);