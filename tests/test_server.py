"""Tests for server.py"""
import pytest
from unittest.mock import patch, MagicMock

from sra_mcp.server import get_config, mcp, SRAConfig


class TestServerModuleImports:
    """Test that server module can be imported"""

    def test_server_module_imports(self):
        """Test that the server module imports without errors"""
        # This will raise ImportError if there are issues
        from sra_mcp import server
        assert server is not None

    def test_mcp_server_exists(self):
        """Test that mcp server instance exists"""
        from sra_mcp.server import mcp
        assert mcp is not None


class TestGetConfig:
    """Test get_config function"""

    def test_get_config_returns_sra_config(self):
        """Test that get_config returns an SRAConfig instance"""
        # Mock SRAConfig.load to return a known config
        mock_config = SRAConfig(sra_path="D:/Games/SRA")

        with patch.object(SRAConfig, 'load', return_value=mock_config) as mock_load:
            # Reset the global _config
            import sra_mcp.server
            sra_mcp.server._config = None

            result = sra_mcp.server.get_config()

            assert isinstance(result, SRAConfig)
            assert result.sra_path == "D:/Games/SRA"
            mock_load.assert_called_once()

    def test_get_config_caches_result(self):
        """Test that get_config caches the config instance"""
        mock_config = SRAConfig(sra_path="D:/Games/SRA")

        with patch.object(SRAConfig, 'load', return_value=mock_config) as mock_load:
            import sra_mcp.server
            sra_mcp.server._config = None

            # First call
            result1 = sra_mcp.server.get_config()
            # Second call
            result2 = sra_mcp.server.get_config()

            # Should only have called load once (cached)
            assert mock_load.call_count == 1
            assert result1 is result2


class TestToolFunctions:
    """Test that tool functions exist and are callable"""

    def test_sra_get_settings_function_exists(self):
        """Test that sra_get_settings function exists"""
        from sra_mcp.server import sra_get_settings
        assert callable(sra_get_settings)

    def test_sra_get_settings_readable_function_exists(self):
        """Test that sra_get_settings_readable function exists"""
        from sra_mcp.server import sra_get_settings_readable
        assert callable(sra_get_settings_readable)

    def test_sra_update_settings_function_exists(self):
        """Test that sra_update_settings function exists"""
        from sra_mcp.server import sra_update_settings
        assert callable(sra_update_settings)

    def test_sra_start_function_exists(self):
        """Test that sra_start function exists"""
        from sra_mcp.server import sra_start
        assert callable(sra_start)

    def test_sra_run_task_function_exists(self):
        """Test that sra_run_task function exists"""
        from sra_mcp.server import sra_run_task
        assert callable(sra_run_task)
