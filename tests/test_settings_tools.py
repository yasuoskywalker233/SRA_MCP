"""Tests for settings MCP tools"""
import json
import pytest
from pathlib import Path
from unittest.mock import mock_open, patch, MagicMock
from sra_mcp.tools.settings import (
    get_settings,
    get_settings_readable,
    update_settings,
    SettingsError,
    SettingsReadError,
    SettingsWriteError,
    InvalidFieldError,
    _get_settings_path,
)


class TestGetSettingsPath:
    def test_get_settings_path(self):
        """Test _get_settings_path returns correct path"""
        path = _get_settings_path()
        assert path.name == "settings.json"
        assert path.parent.name == "SRA"


class TestGetSettings:
    def test_get_settings_file_not_found(self):
        """Test SettingsReadError is raised when file does not exist"""
        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/nonexistent/settings.json")
            with patch("builtins.open", mock_open()) as mock_file:
                mock_file.return_value.read.side_effect = FileNotFoundError()
                with pytest.raises(SettingsReadError) as exc_info:
                    get_settings()
                assert "Settings file not found" in str(exc_info.value)

    def test_get_settings_invalid_json(self):
        """Test SettingsReadError is raised when JSON is invalid"""
        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/invalid/settings.json")
            with patch("builtins.open", mock_open()) as mock_file:
                mock_file.return_value.read.side_effect = json.JSONDecodeError(
                    "Invalid JSON", "", 0
                )
                with pytest.raises(SettingsReadError) as exc_info:
                    get_settings()
                assert "Invalid JSON" in str(exc_info.value)

    def test_get_settings_success(self):
        """Test successful settings read"""
        test_data = {"language": 0, "isDeveloperMode": False}
        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/test/settings.json")
            with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                result = get_settings()
                assert result == test_data


class TestGetSettingsReadable:
    def test_get_settings_readable_success(self):
        """Test get_settings_readable returns both raw and readable formats"""
        test_data = {
            "language": 0,
            "isDeveloperMode": False,
            "allowNotifications": True,
        }
        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/test/settings.json")
            with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                result = get_settings_readable()
                assert "raw" in result
                assert "readable" in result
                assert result["raw"] == test_data
                # Check readable format has correct structure
                readable = result["readable"]
                assert "语言" in readable
                assert "允许通知" in readable


class TestUpdateSettings:
    def test_update_settings_invalid_field(self):
        """Test InvalidFieldError is raised for unknown field names"""
        test_data = {"language": 0}
        updates = {"无效字段": "some_value"}

        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/test/settings.json")
            with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                with pytest.raises(InvalidFieldError) as exc_info:
                    update_settings(updates)
                assert "Unknown fields" in str(exc_info.value)

    def test_update_settings_file_not_found(self):
        """Test SettingsReadError is raised when file does not exist"""
        updates = {"语言": "English"}

        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/nonexistent/settings.json")
            with patch("builtins.open", mock_open()) as mock_file:
                mock_file.return_value.read.side_effect = FileNotFoundError()
                with pytest.raises(SettingsReadError):
                    update_settings(updates)

    def test_update_settings_invalid_json_on_read(self):
        """Test SettingsReadError is raised when existing file has invalid JSON"""
        updates = {"语言": "English"}

        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/invalid/settings.json")
            with patch("builtins.open", mock_open()) as mock_file:
                mock_file.return_value.read.side_effect = json.JSONDecodeError(
                    "Invalid JSON", "", 0
                )
                with pytest.raises(SettingsReadError):
                    update_settings(updates)

    def test_update_settings_success(self):
        """Test successful settings update"""
        original_data = {
            "language": 0,
            "isDeveloperMode": False,
            "allowNotifications": True,
        }
        updates = {"语言": "English"}

        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/test/settings.json")
            m = mock_open(read_data=json.dumps(original_data))
            with patch("builtins.open", m):
                result = update_settings(updates)
                # Verify the update was applied (language should be 1 for English)
                assert result["language"] == 1
                # Verify other fields are preserved
                assert result["isDeveloperMode"] is False
                assert result["allowNotifications"] is True

    def test_update_settings_multiple_fields(self):
        """Test updating multiple fields at once"""
        original_data = {
            "language": 0,
            "isDeveloperMode": False,
            "allowNotifications": False,
            "smtpPort": 587,
        }
        updates = {
            "语言": "English",
            "开发者模式": "是",
        }

        with patch("sra_mcp.tools.settings._get_settings_path") as mock_path:
            mock_path.return_value = Path("/test/settings.json")
            m = mock_open(read_data=json.dumps(original_data))
            with patch("builtins.open", m):
                result = update_settings(updates)
                assert result["language"] == 1  # English
                assert result["isDeveloperMode"] is True
                # Original fields should be preserved
                assert result["allowNotifications"] is False
                assert result["smtpPort"] == 587


class TestSettingsErrorClasses:
    def test_settings_error_inheritance(self):
        """Test that all error classes inherit properly"""
        assert issubclass(SettingsReadError, SettingsError)
        assert issubclass(SettingsWriteError, SettingsError)
        assert issubclass(InvalidFieldError, SettingsError)

    def test_settings_read_error_message(self):
        """Test SettingsReadError can be instantiated with message"""
        error = SettingsReadError("Test error message")
        assert str(error) == "Test error message"

    def test_settings_write_error_message(self):
        """Test SettingsWriteError can be instantiated with message"""
        error = SettingsWriteError("Test error message")
        assert str(error) == "Test error message"

    def test_invalid_field_error_message(self):
        """Test InvalidFieldError can be instantiated with message"""
        error = InvalidFieldError("Test error message")
        assert str(error) == "Test error message"