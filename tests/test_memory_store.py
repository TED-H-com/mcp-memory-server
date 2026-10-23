import pytest
import sqlite3
import json
import re
from mcp_memory.server import mcp

@pytest.mark.asyncio
async def test_memory_store_decision():
    """Test storing a decision automatically classifies and inserts correctly."""
    result = await mcp.call_tool("memory_store", {
        "content": "decided to use python | we need a scripting language | good library ecosystem",
        "type": "auto"
    })

    assert not result.is_error
    content_text = result.content[0].text
    assert "Decision recorded" in content_text

    # Extract ID from the result string (e.g. "(id: 1234abcd)")
    import re
    match = re.search(r"\(id: ([a-z0-9]+)\)", content_text)
    assert match is not None
    record_id = match.group(1)

    # Verify in DB via get tool
    get_res = await mcp.call_tool("memory_get", {"id": record_id})
    assert not get_res.is_error
    assert record_id in get_res.content[0].text
    assert "decided to use python" in get_res.content[0].text
    assert "we need a scripting language" in get_res.content[0].text

@pytest.mark.asyncio
async def test_memory_store_question():
    """Test storing a question automatically classifies and inserts correctly."""
    result = await mcp.call_tool("memory_store", {
        "content": "how to connect to the db?",
        "type": "auto"
    })

    assert not result.is_error
    content_text = result.content[0].text
    assert "Question recorded" in content_text

    match = re.search(r"\(id: ([a-z0-9]+)\)", content_text)
    assert match is not None
    record_id = match.group(1)

    get_res = await mcp.call_tool("memory_get", {"id": record_id})
    assert not get_res.is_error
    assert "how to connect to the db?" in get_res.content[0].text

@pytest.mark.asyncio
async def test_memory_store_knowledge():
    """Test storing a knowledge item automatically classifies and inserts correctly."""
    result = await mcp.call_tool("memory_store", {
        "content": "This is a random fact about space that we learned today.",
        "type": "auto"
    })

    assert not result.is_error
    content_text = result.content[0].text
    assert "Knowledge recorded" in content_text

    match = re.search(r"\(id: ([a-z0-9]+)\)", content_text)
    assert match is not None
    record_id = match.group(1)

    get_res = await mcp.call_tool("memory_get", {"id": record_id})
    assert not get_res.is_error
    assert "This is a random fact about space that we learned today." in get_res.content[0].text

@pytest.mark.asyncio
async def test_memory_list():
    """Test that listing memories works correctly."""
    # First, clear anything from the mock DB for this test if possible, or just insert something fresh
    await mcp.call_tool("memory_store", {
        "content": "A special test decision | context | how",
        "type": "decision"
    })

    list_res = await mcp.call_tool("memory_list", {"type": "decisions"})
    assert not list_res.is_error
    content_text = list_res.content[0].text
    assert "A special test decision" in content_text

@pytest.mark.asyncio
async def test_memory_delete():
    """Test deleting a memory by ID."""
    result = await mcp.call_tool("memory_store", {
        "content": "A memory to be deleted",
        "type": "knowledge"
    })

    match = re.search(r"\(id: ([a-z0-9]+)\)", result.content[0].text)
    assert match is not None
    record_id = match.group(1)

    # Verify it exists
    get_res = await mcp.call_tool("memory_get", {"id": record_id})
    assert record_id in get_res.content[0].text

    # Delete it
    del_res = await mcp.call_tool("memory_delete", {"id": record_id})
    assert not del_res.is_error
    assert f"Deleted '{record_id}'" in del_res.content[0].text

    # Verify it's gone
    get_res2 = await mcp.call_tool("memory_get", {"id": record_id})
    assert f"Memory '{record_id}' not found" in get_res2.content[0].text

@pytest.mark.asyncio
async def test_memory_get_summary():
    """Test getting a summary of memory operations."""
    await mcp.call_tool("memory_store", {"content": "Summary decision | a | b", "type": "decision"})

    summary_res = await mcp.call_tool("memory_get_summary", {})
    assert not summary_res.is_error
    content_text = summary_res.content[0].text

    assert "[test-ws] Decisions:" in content_text
    assert "Resolved:" in content_text
    assert "Questions:" in content_text
    assert "Knowledge:" in content_text
