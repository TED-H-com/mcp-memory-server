import pytest
import asyncio
from mcp_memory.server import mcp

@pytest.mark.asyncio
async def test_list_tools():
    """Test that all expected tools are registered and listed."""
    tools = await mcp.list_tools() if asyncio.iscoroutinefunction(mcp.list_tools) else mcp.list_tools()

    # FastMCP list_tools returns a list of Tool objects. Let's get their names.
    tool_names = [t.name for t in tools]

    expected_tools = [
        "memory_store",
        "memory_record_decision",
        "memory_record_resolved",
        "memory_record_question",
        "memory_record_knowledge",
        "memory_list",
        "memory_get",
        "memory_get_summary",
        "memory_delete",
        "memory_search",
        "memory_reinforce",
        "memory_audit_search",
        "memory_audit_stats",
        "memory_daily_report",
        "memory_activity_log",
        "memory_status",
        "memory_compact",
        "memory_oracle_summary",
    ]

    for expected in expected_tools:
        assert expected in tool_names, f"Expected tool {expected} not found in tools list."

@pytest.mark.asyncio
async def test_call_tool():
    """Test calling a tool via MCP handler properly routes it."""
    # We call memory_status which does not require arguments
    result = await mcp.call_tool("memory_status", {})

    # Result from FastMCP is a list of TextContent objects.
    # fastmcp versions can vary the structure, but we can verify it ran without errors
    assert not result.is_error, "Tool call returned an error"

    # We can check that the content contains expected output
    content_text = result.content[0].text
    assert "MCP Memory Server" in content_text
    assert "Workspace: test-ws" in content_text
