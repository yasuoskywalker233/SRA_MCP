"""Tests for config.py"""
import json
import os
import tempfile
from pathlib import Path

import pytest

from sra_mcp.config import (
    ConfigNotFoundError,
    ConfigReadError,
    SRAConfig,
)


class TestLoadConfigSuccess:
    """Test successful config loading"""

    def test_load_config_success(self, tmp_path):
        """Test successfully loading a valid config.json"""
        config_data = {"sra_path": "D:/Games/SRA"}
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

        config = SRAConfig.load(config_file)

        assert config.sra_path == "D:/Games/SRA"

    def test_load_config_string_path(self, tmp_path):
        """Test loading with string path"""
        config_data = {"sra_path": "D:/Games/SRA"}
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

        config = SRAConfig.load(str(config_file))

        assert config.sra_path == "D:/Games/SRA"


class TestLoadConfigNotFound:
    """Test config file not found scenarios"""

    def test_load_config_not_found(self):
        """Test that ConfigNotFoundError is raised when config file does not exist"""
        with pytest.raises(ConfigNotFoundError):
            SRAConfig.load("/nonexistent/path/config.json")

    def test_load_config_no_search_paths(self, monkeypatch, tmp_path):
        """Test search falls back to module-relative path when no config in cwd"""
        # Create a temp dir and change to it
        monkeypatch.chdir(tmp_path)

        # Should NOT raise - module-relative search finds config in project root
        config = SRAConfig.load()
        assert config.sra_path == "D:\\work\\SRA\\SRA_Release"


class TestLoadConfigInvalidJson:
    """Test invalid JSON handling"""

    def test_load_config_invalid_json(self, tmp_path):
        """Test that ConfigReadError is raised for invalid JSON"""
        config_file = tmp_path / "config.json"
        config_file.write_text("{ invalid json }", encoding="utf-8")

        with pytest.raises(ConfigReadError):
            SRAConfig.load(config_file)


class TestSRAConfigPaths:
    """Test path helper methods"""

    def test_get_sra_exe_path(self):
        """Test get_sra_exe_path returns correct path"""
        config = SRAConfig(sra_path="D:/Games/SRA")
        assert config.get_sra_exe_path() == Path("D:/Games/SRA/SRA.exe")

    def test_get_sra_cli_exe_path(self):
        """Test get_sra_cli_exe_path returns correct path"""
        config = SRAConfig(sra_path="D:/Games/SRA")
        assert config.get_sra_cli_exe_path() == Path("D:/Games/SRA/SRA-cli.exe")

    def test_get_settings_path(self, monkeypatch):
        """Test get_settings_path returns correct APPDATA path"""
        monkeypatch.setenv("APPDATA", "D:/AppData/Roaming")
        config = SRAConfig(sra_path="D:/Games/SRA")
        assert config.get_settings_path() == Path("D:/AppData/Roaming/SRA/settings.json")

    def test_get_configs_dir(self, monkeypatch):
        """Test get_configs_dir returns correct APPDATA path"""
        monkeypatch.setenv("APPDATA", "D:/AppData/Roaming")
        config = SRAConfig(sra_path="D:/Games/SRA")
        assert config.get_configs_dir() == Path("D:/AppData/Roaming/SRA/configs")