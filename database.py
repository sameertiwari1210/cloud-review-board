# ==============================================================================
# Database Module — Phase 6: SQLite Persistence
# ==============================================================================
# Why: Replaces ephemeral JSON memory with a structured SQLite database so that
#      every review run is persisted, queryable, and replayable.
# Technology: Python standard library `sqlite3` — no external dependencies.

import os
import sqlite3
from datetime import datetime

# Path to the SQLite database file inside the data/ directory.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "csrb.db")


# Why: Returns a fresh database connection to the SQLite file.
# Inputs: None
# Outputs: sqlite3.Connection — open connection to csrb.db.
def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


# Why: Creates all required tables if they do not already exist.
#      Called once at application startup.
# Inputs: None
# Outputs: None
def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # conversations: one row per user session / question
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            query     TEXT    NOT NULL,
            started_at TEXT   NOT NULL
        )
    """)

    # agent_outputs: one row per agent per conversation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_outputs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            agent_name      TEXT    NOT NULL,
            output          TEXT    NOT NULL,
            created_at      TEXT    NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # user_preferences: key-value store for persistent settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"[DB] SQLite database initialised at: {DB_PATH}")


# Why: Inserts a new conversation record and returns its auto-generated ID.
# Inputs:
#   - query (str): The user's original question.
# Outputs:
#   - int: The new conversation's primary key ID.
def save_conversation(query: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (query, started_at) VALUES (?, ?)",
        (query, datetime.utcnow().isoformat())
    )
    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    return conversation_id


# Why: Saves an individual agent's output tied to a specific conversation.
# Inputs:
#   - conversation_id (int): The parent conversation's primary key.
#   - agent_name (str): Human-readable agent label (e.g. "Architect").
#   - output (str): The full text output from the agent.
# Outputs: None
def save_agent_output(conversation_id: int, agent_name: str, output: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO agent_outputs
           (conversation_id, agent_name, output, created_at)
           VALUES (?, ?, ?, ?)""",
        (conversation_id, agent_name, output, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


# Why: Retrieves the N most recent conversations with all their agent outputs
#      so the user can replay or review past sessions.
# Inputs:
#   - limit (int): Maximum number of past conversations to return.
# Outputs:
#   - list[dict]: Each entry has keys: id, query, started_at, outputs (list).
def load_history(limit: int = 5) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, query, started_at FROM conversations ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    convs = cursor.fetchall()

    history = []
    for conv in convs:
        cursor.execute(
            "SELECT agent_name, output, created_at FROM agent_outputs WHERE conversation_id = ?",
            (conv["id"],)
        )
        outputs = [dict(row) for row in cursor.fetchall()]
        history.append({
            "id": conv["id"],
            "query": conv["query"],
            "started_at": conv["started_at"],
            "outputs": outputs
        })

    conn.close()
    return history


# Why: Upserts a user preference key-value pair into the persistent store.
# Inputs:
#   - key (str): The preference name (e.g. "preferred_cloud").
#   - value (str): The preference value (e.g. "AWS").
# Outputs: None
def save_preference(key: str, value: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_preferences (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value)
    )
    conn.commit()
    conn.close()


# Why: Fetches all stored user preferences as a dictionary.
# Inputs: None
# Outputs: dict — preference key-value pairs.
def load_preferences() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM user_preferences")
    rows = cursor.fetchall()
    conn.close()
    return {row["key"]: row["value"] for row in rows}
