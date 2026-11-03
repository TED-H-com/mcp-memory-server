import pytest
import time
from mcp_memory.server import memory_get_summary, memory_get, memory_search, memory_list, _local_text_search
from mcp_memory.db import get_sqlite
import mcp_memory.db as db
import sqlite3
import uuid
import os

@pytest.fixture
def test_workspace(tmp_path, monkeypatch):
    ws_dir = tmp_path / "workspace" / ".claude-memory"
    ws_dir.mkdir(parents=True)
    db_path = ws_dir / "memory.db"

    conn = sqlite3.connect(str(db_path))
    conn.executescript("""
        CREATE TABLE decisions (id TEXT PRIMARY KEY, date TEXT, what TEXT, why TEXT, how TEXT, tags TEXT, status TEXT, created_at TEXT DEFAULT (datetime('now')), access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0);
        CREATE TABLE resolved (id TEXT PRIMARY KEY, what TEXT, how TEXT, tags TEXT, date TEXT DEFAULT (date('now')), created_at TEXT DEFAULT (datetime('now')), access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0);
        CREATE TABLE open_questions (id TEXT PRIMARY KEY, question TEXT, context TEXT, tags TEXT, priority INTEGER DEFAULT 2, raised TEXT DEFAULT (datetime('now')), created_at TEXT DEFAULT (datetime('now')), access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0);
        CREATE TABLE knowledge_items (id TEXT PRIMARY KEY, title TEXT, content TEXT, tags TEXT, written_to_obsidian INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')), access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0);
        CREATE TABLE daily_logs (id TEXT PRIMARY KEY);
    """)

    # Insert 10,000 items
    knowledge_items = []
    for i in range(10000):
        id_ = str(uuid.uuid4())[:8]
        knowledge_items.append((id_, f"title {i}", f"content {i} test data", "[]", 0, 1.0))

    conn.executemany("INSERT INTO knowledge_items (id, title, content, tags, written_to_obsidian, salience) VALUES (?, ?, ?, ?, ?, ?)", knowledge_items)
    conn.commit()
    conn.close()

    # mock config to return this db
    monkeypatch.setenv("MEMORY_WORKSPACE", "test-ws")

    monkeypatch.setattr(db, "load_config", lambda: {
        "workspace_root": str(tmp_path),
        "workspace_map": str(tmp_path / "map.json"),
        "oracle": {"enabled": False},
        "embedding": {"provider": "none"}
    })

    with open(tmp_path / "map.json", "w") as f:
        f.write('{"test-ws": "workspace"}')


    return "test-ws"

def test_benchmark_summary(test_workspace, benchmark):
    def run_summary():
        memory_get_summary(test_workspace)
    benchmark(run_summary)

def test_benchmark_search(test_workspace, benchmark):
    def run_search():
        _local_text_search("test data", limit=50)
    benchmark(run_search)
