# ==============================================================================
# Document Loader — Phase 7: Local RAG (Retrieval-Augmented Generation)
# ==============================================================================
# Why: Enables agents to query local knowledge files without any vector database
#      or internet connection. Uses pure keyword search against SQLite-stored
#      text chunks to retrieve relevant context for agent prompts.

import os
import re
import sqlite3
from database import get_connection, DB_PATH

# Path to the knowledge/ directory relative to this file.
KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge")

# Target chunk size in approximate word count.
CHUNK_SIZE_WORDS = 150


# Why: Reads all .md and .txt files from the knowledge/ directory.
# Inputs: None
# Outputs:
#   - list[dict]: Each entry has keys 'source' (filename) and 'content' (raw text).
def load_documents() -> list:
    docs = []
    if not os.path.isdir(KNOWLEDGE_DIR):
        print(f"[RAG] WARNING: knowledge/ directory not found at {KNOWLEDGE_DIR}")
        return docs

    for filename in os.listdir(KNOWLEDGE_DIR):
        if filename.endswith((".md", ".txt")):
            filepath = os.path.join(KNOWLEDGE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            docs.append({"source": filename, "content": content})
            print(f"[RAG] Loaded document: {filename} ({len(content)} chars)")

    return docs


# Why: Splits a long text into smaller chunks of approximately CHUNK_SIZE_WORDS
#      words so that each chunk fits comfortably inside an LLM prompt.
# Inputs:
#   - text (str): The raw document text to chunk.
#   - source (str): The source filename, used as metadata per chunk.
# Outputs:
#   - list[dict]: Each entry has keys 'source', 'chunk_index', 'content'.
def chunk_text(text: str, source: str) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), CHUNK_SIZE_WORDS):
        chunk_words = words[i: i + CHUNK_SIZE_WORDS]
        chunks.append({
            "source": source,
            "chunk_index": i // CHUNK_SIZE_WORDS,
            "content": " ".join(chunk_words)
        })
    return chunks


# Why: Creates the knowledge_chunks table and inserts all document chunks.
#      Called once (or after knowledge files change) to populate the RAG index.
# Inputs: None
# Outputs: None
def store_chunks() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_chunks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source      TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content     TEXT NOT NULL
        )
    """)

    # Clear old chunks to allow fresh reloading
    cursor.execute("DELETE FROM knowledge_chunks")

    docs = load_documents()
    total = 0
    for doc in docs:
        chunks = chunk_text(doc["content"], doc["source"])
        for chunk in chunks:
            cursor.execute(
                "INSERT INTO knowledge_chunks (source, chunk_index, content) VALUES (?, ?, ?)",
                (chunk["source"], chunk["chunk_index"], chunk["content"])
            )
            total += 1

    conn.commit()
    conn.close()
    print(f"[RAG] Stored {total} chunks from {len(docs)} documents into SQLite.")


# Why: Searches knowledge_chunks for chunks that contain any of the query keywords.
#      Returns the top N most relevant chunks to inject into agent prompts.
# Inputs:
#   - query (str): The user's question; keywords are extracted by splitting on whitespace.
#   - top_n (int): Maximum number of chunks to return (default 3).
# Outputs:
#   - str: Concatenated chunk content, ready to prepend to an agent system prompt.
def keyword_search(query: str, top_n: int = 3) -> str:
    # Extract meaningful keywords (longer than 3 chars, lowercased)
    keywords = [w.lower() for w in re.split(r"\W+", query) if len(w) > 3]
    if not keywords:
        return ""

    conn = get_connection()
    cursor = conn.cursor()

    # Check if knowledge_chunks table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_chunks'"
    )
    if not cursor.fetchone():
        conn.close()
        return ""

    # Score each chunk by how many keywords it contains
    cursor.execute("SELECT id, source, content FROM knowledge_chunks")
    rows = cursor.fetchall()
    conn.close()

    scored = []
    for row in rows:
        content_lower = row["content"].lower()
        score = sum(1 for kw in keywords if kw in content_lower)
        if score > 0:
            scored.append((score, row["source"], row["content"]))

    # Sort by score descending, take top_n
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = scored[:top_n]

    if not top_chunks:
        return ""

    parts = ["# Relevant Knowledge Base Context\n"]
    for score, source, content in top_chunks:
        parts.append(f"[Source: {source}]\n{content}\n")

    return "\n".join(parts)
