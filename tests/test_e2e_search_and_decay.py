import pytest
import json
import re
from unittest.mock import patch, mock_open
from mcp_memory.server import mcp, run_decay

@pytest.mark.asyncio
async def test_e2e_search_salience_ranking(mock_db, test_workspace):
    """Test that search results are ranked correctly by salience."""
    # Insert 3 items with different salience
    mock_db.execute(
        "INSERT INTO knowledge_items (id, title, content, salience) VALUES (?, ?, ?, ?)",
        ("id1", "item 1", "searchterm here", 1.0)
    )
    mock_db.execute(
        "INSERT INTO knowledge_items (id, title, content, salience) VALUES (?, ?, ?, ?)",
        ("id2", "item 2", "searchterm here", 2.0)
    )
    mock_db.execute(
        "INSERT INTO knowledge_items (id, title, content, salience) VALUES (?, ?, ?, ?)",
        ("id3", "item 3", "searchterm here", 1.5)
    )
    mock_db.commit()

    mock_config = {
        "workspace_map": "/tmp/dummy_workspace_map.json",
        "workspace_root": "/tmp/ws",
        "claude_setup_dir": "/tmp/claude"
    }
    mock_ws_map = json.dumps({test_workspace: "test-dir"})

    with patch("mcp_memory.config.load_config", return_value=mock_config), \
         patch("builtins.open", mock_open(read_data=mock_ws_map)):

        search_res = await mcp.call_tool("memory_search", {"query": "searchterm"})
        assert not search_res.is_error

        content_text = search_res.content[0].text

        # Verify ordering in output text
        idx2 = content_text.find("id2")
        idx3 = content_text.find("id3")
        idx1 = content_text.find("id1")

        assert idx2 != -1
        assert idx3 != -1
        assert idx1 != -1

        # Because salience 2.0 > 1.5 > 1.0, id2 should be before id3, and id3 before id1
        assert idx2 < idx3
        assert idx3 < idx1

def test_e2e_salience_decay(mock_db, test_workspace):
    """Test that only stale memories have their salience decayed."""
    # Insert a recent item
    mock_db.execute(
        "INSERT INTO knowledge_items (id, title, content, created_at, last_accessed, salience) VALUES (?, ?, ?, datetime('now'), datetime('now'), ?)",
        ("recent_id", "recent item", "content", 1.0)
    )
    # Insert a stale item (40 days old)
    mock_db.execute(
        "INSERT INTO knowledge_items (id, title, content, created_at, last_accessed, salience) VALUES (?, ?, ?, datetime('now', '-40 days'), datetime('now', '-40 days'), ?)",
        ("stale_id", "stale item", "content", 1.0)
    )
    mock_db.commit()

    # Run decay
    run_decay(workspace_id=test_workspace, decay_factor=0.5, stale_days=30)

    # Check new saliences
    recent_row = mock_db.execute("SELECT salience FROM knowledge_items WHERE id = 'recent_id'").fetchone()
    stale_row = mock_db.execute("SELECT salience FROM knowledge_items WHERE id = 'stale_id'").fetchone()

    assert recent_row["salience"] == 1.0
    assert stale_row["salience"] == 0.5
