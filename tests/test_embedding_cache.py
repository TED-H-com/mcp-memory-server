import pytest
from unittest.mock import MagicMock
from mcp_memory.server import _get_embedding, _embedding_cache
import mcp_memory.config

def test_get_embedding_cache():
    # Clear cache before testing
    _embedding_cache.clear()

    # Mock openai client
    import sys
    from unittest.mock import patch
    mock_openai = MagicMock()
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
    mock_client.embeddings.create.return_value = mock_resp
    mock_openai.OpenAI.return_value = mock_client

    with patch('mcp_memory.config.load_config') as mock_load_config:
        mock_load_config.return_value = {
            "embedding": {"provider": "openai", "api_key": "fake", "model": "text-embedding-3-small"}
        }
        with patch.dict('sys.modules', {'openai': mock_openai}):
            # Test successful embedding is cached
            res1 = _get_embedding("test success")
            assert res1 == [0.1, 0.2, 0.3]
            assert ("openai", "text-embedding-3-small", "test success") in _embedding_cache
            assert mock_client.embeddings.create.call_count == 1

            # Test second call uses cache (call_count should not increase)
            res2 = _get_embedding("test success")
            assert res2 == [0.1, 0.2, 0.3]
            assert mock_client.embeddings.create.call_count == 1

            # Test failed embedding (exception) is not cached
            mock_client.embeddings.create.side_effect = Exception("API error")
            res_fail = _get_embedding("test fail")
            assert res_fail is None
            assert ("openai", "text-embedding-3-small", "test fail") not in _embedding_cache
            assert mock_client.embeddings.create.call_count == 2

            # Second call to failed should hit API again (call_count increases)
            res_fail2 = _get_embedding("test fail")
            assert res_fail2 is None
            assert mock_client.embeddings.create.call_count == 3
