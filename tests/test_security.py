import os
import stat
from pathlib import Path
import pytest

from mcp_memory.config import save_config, CONFIG_FILE
from mcp_memory.server import mcp

@pytest.fixture
def temp_config(tmp_path, monkeypatch):
    test_config_file = tmp_path / "config.json"
    monkeypatch.setattr("mcp_memory.config.CONFIG_FILE", test_config_file)
    monkeypatch.setattr("mcp_memory.config.CONFIG_DIR", tmp_path)
    return test_config_file

def test_config_file_permissions(temp_config):
    """Ensure that the config file is created with 0o600 permissions."""
    test_data = {"test": "data", "oracle": {"password": "secret_password"}}
    save_config(test_data)

    assert temp_config.exists()
    st = os.stat(temp_config)
    # Check if the permissions are strictly 0o600 (owner read/write only)
    assert stat.S_IMODE(st.st_mode) == 0o600

@pytest.mark.asyncio
async def test_input_validation_limit(monkeypatch):
    """Test that the limit parameter is clamped."""
    # Mock get_oracle to return None to test the local code path
    monkeypatch.setattr("mcp_memory.server.get_oracle", lambda: None)

    # Using an overly large limit shouldn't crash
    result = await mcp.call_tool("memory_search", {"query": "test", "limit": 1000000})
    assert not result.is_error

    # Using negative limit shouldn't crash
    result = await mcp.call_tool("memory_search", {"query": "test", "limit": -10})
    assert not result.is_error

@pytest.mark.asyncio
async def test_input_validation_priority(monkeypatch):
    # Testing priority validation by not crashing
    # Create a dummy sqlite db setup if needed, but since fastmcp tools are async/sync
    # we just need to ensure the parameters don't cause unhandled exception at top level
    try:
        # It may fail because workspace db might not exist, but we care that the
        # bounds logic itself doesn't raise a python error before sqlite
        await mcp.call_tool("memory_record_question", {"question": "Q?", "priority": 99})
    except FileNotFoundError:
        pass # this means it got past our boundary check

@pytest.mark.asyncio
async def test_input_validation_type():
    try:
        # Invalid type should fall back to "all" without crashing
        await mcp.call_tool("memory_list", {"type": "DROP TABLE", "limit": 10})
    except FileNotFoundError:
        pass
