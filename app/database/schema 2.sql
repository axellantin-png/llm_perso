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