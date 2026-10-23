import pytest
import sqlite3
from unittest.mock import patch
import json

class MockConnection(sqlite3.Connection):
    def close(self):
        # Prevent the connection from closing so it persists across multiple tool calls in memory
        pass

@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:", factory=MockConnection, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE decisions (
            id TEXT PRIMARY KEY, date TEXT DEFAULT (date('now')), what TEXT NOT NULL,
            why TEXT, how TEXT, tags TEXT, status TEXT, created_at TEXT DEFAULT (datetime('now')),
            access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0
        );
        CREATE TABLE resolved (
            id TEXT PRIMARY KEY, what TEXT NOT NULL, how TEXT, tags TEXT,
            date TEXT DEFAULT (date('now')), created_at TEXT DEFAULT (datetime('now')),
            access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0
        );
        CREATE TABLE open_questions (
            id TEXT PRIMARY KEY, question TEXT NOT NULL, context TEXT, tags TEXT,
            priority INTEGER DEFAULT 2, raised TEXT DEFAULT (datetime('now')),
            created_at TEXT DEFAULT (datetime('now')), access_count INTEGER DEFAULT 0,
            last_accessed TEXT, salience REAL DEFAULT 1.0
        );
        CREATE TABLE knowledge_items (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT, tags TEXT,
            written_to_obsidian INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')),
            access_count INTEGER DEFAULT 0, last_accessed TEXT, salience REAL DEFAULT 1.0
        );
        CREATE TABLE daily_logs (id TEXT PRIMARY KEY);
    """)
    yield conn

    # We explicitly close the base connection when the test is done
    sqlite3.Connection.close(conn)

@pytest.fixture
def test_workspace():
    return "test-ws"

@pytest.fixture(autouse=True)
def mock_dependencies(mock_db, test_workspace):
    with patch("mcp_memory.server.get_sqlite", return_value=mock_db), \
         patch("mcp_memory.server.detect_workspace", return_value=test_workspace):
        yield mock_db
