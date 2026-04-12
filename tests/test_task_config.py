"""Tests for task config tools"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from sra_mcp.tools.task_config import (
    get_task_config,
    get_task_config_readable,
    update_task_config,
    list_task_configs,
    TaskConfigNotFoundError,
    TaskConfigReadError,
    TaskConfigWriteError,
    InvalidTaskFieldError,
)
from sra_mcp.task_config_mappings import (
    TASK_CONFIG_FIELDS,
    TaskConfigJsonToDisplayMapper,
    TaskConfigDisplayToJsonMapper,
)


class TestTaskConfigJsonToDisplayMapper:
    """Tests for TaskConfigJsonToDisplayMapper"""

    def test_map_enabled_tasks(self):
        """Test mapping of EnabledTasks array"""
        mapper = TaskConfigJsonToDisplayMapper()
        raw = {
            "EnabledTasks": [True, False, True, False, False],
            "Name": "TestConfig"
        }
        result = mapper.map(raw)

        assert "启用启动游戏" in result
        assert result["启用启动游戏"]["value"] is True
        assert result["启用启动游戏"]["display"] == "是"

        assert "启用清体力" in result
        assert result["启用清体力"]["value"] is False
        assert result["启用清体力"]["display"] == "否"

    def test_map_receive_rewards(self):
        """Test mapping of ReceiveRewards array"""
        mapper = TaskConfigJsonToDisplayMapper()
        raw = {
            "ReceiveRewards": [True, True, False, True, False, True, False],
            "Name": "TestConfig"
        }
        result = mapper.map(raw)

        assert "领取每日实训" in result
        assert result["领取每日实训"]["value"] is True
        assert result["领取每日实训"]["display"] == "是"

        assert "领取助战奖励" in result
        assert result["领取助战奖励"]["value"] is False
        assert result["领取助战奖励"]["display"] == "否"

    def test_map_bool_field(self):
        """Test mapping of bool fields"""
        mapper = TaskConfigJsonToDisplayMapper()
        raw = {
            "DUEnable": True,
            "CurrencyWarsEnable": False,
            "Name": "Test"
        }
        result = mapper.map(raw)

        assert "启用差分宇宙" in result
        assert result["启用差分宇宙"]["value"] is True
        assert result["启用差分宇宙"]["display"] == "是"

        assert "启用货币战争" in result
        assert result["启用货币战争"]["value"] is False
        assert result["启用货币战争"]["display"] == "否"

    def test_map_int_field_with_options(self):
        """Test mapping of int fields with options"""
        mapper = TaskConfigJsonToDisplayMapper()
        raw = {
            "CurrencyWarsMode": 0,
            "CurrencyWarsDifficulty": 2,
            "Name": "Test"
        }
        result = mapper.map(raw)

        assert result["货币战争模式"]["display"] == "标准博弈"
        assert result["货币战争难度"]["display"] == "当前难度"

    def test_map_str_field(self):
        """Test mapping of string fields"""
        mapper = TaskConfigJsonToDisplayMapper()
        raw = {
            "StartGameUsername": "test_user",
            "CurrencyWarsUsername": "honkai_player",
            "Name": "Test"
        }
        result = mapper.map(raw)

        assert "启动用户名" in result
        assert result["启动用户名"]["value"] == "test_user"
        assert "货币战争用户名" in result
        assert result["货币战争用户名"]["value"] == "honkai_player"

    def test_map_task_list(self):
        """Test mapping of TrailblazePowerTaskList"""
        mapper = TaskConfigJsonToDisplayMapper()
        raw = {
            "TrailblazePowerTaskList": [
                {"Name": "Task1", "Level": 1},
                {"Name": "Task2", "Level": 2},
            ],
            "Name": "Test"
        }
        result = mapper.map(raw)

        assert "清体力任务列表" in result
        assert result["清体力任务列表"]["display"] == "2 个关卡"


class TestTaskConfigDisplayToJsonMapper:
    """Tests for TaskConfigDisplayToJsonMapper"""

    def test_map_bool_to_enabled_tasks(self):
        """Test mapping bool display values to EnabledTasks array"""
        mapper = TaskConfigDisplayToJsonMapper()
        display = {
            "启用启动游戏": "是",
            "启用清体力": "否",
            "启用领取奖励": "是",
        }
        result = mapper.map(display)

        assert "EnabledTasks" in result
        assert result["EnabledTasks"][0] is True
        assert result["EnabledTasks"][1] is False
        assert result["EnabledTasks"][2] is True

    def test_map_bool_to_receive_rewards(self):
        """Test mapping bool display values to ReceiveRewards array"""
        mapper = TaskConfigDisplayToJsonMapper()
        display = {
            "领取每日实训": "是",
            "领取无名勋礼": "否",
        }
        result = mapper.map(display)

        assert "ReceiveRewards" in result
        assert result["ReceiveRewards"][0] is True
        assert result["ReceiveRewards"][1] is False

    def test_map_int_with_options(self):
        """Test mapping int display values with options"""
        mapper = TaskConfigDisplayToJsonMapper()
        display = {
            "货币战争模式": "超频博弈",
            "货币战争难度": "最高难度",
        }
        result = mapper.map(display)

        assert result["CurrencyWarsMode"] == 1
        assert result["CurrencyWarsDifficulty"] == 1

    def test_map_str_field(self):
        """Test mapping string fields"""
        mapper = TaskConfigDisplayToJsonMapper()
        display = {
            "启动用户名": "test_user",
            "货币战争用户名": "player123",
        }
        result = mapper.map(display)

        assert result["StartGameUsername"] == "test_user"
        assert result["CurrencyWarsUsername"] == "player123"

    def test_unknown_field_ignored(self):
        """Test that unknown fields are ignored"""
        mapper = TaskConfigDisplayToJsonMapper()
        display = {
            "未知字段": "some_value",
            "启用清体力": "是",
        }
        result = mapper.map(display)

        assert "未知字段" not in result
        assert result["EnabledTasks"][1] is True


class TestTaskConfigTools:
    """Tests for task config tools functions"""

    def test_get_task_config_file_not_found(self, tmp_path):
        """Test get_task_config raises error when file not found"""
        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with pytest.raises(TaskConfigNotFoundError):
            get_task_config("NonExistent", mock_config)

    def test_get_task_config_invalid_json(self, tmp_path):
        """Test get_task_config raises error when JSON is invalid"""
        config_file = tmp_path / "TestConfig.json"
        config_file.write_text("invalid json {")

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with pytest.raises(TaskConfigReadError):
            get_task_config("TestConfig", mock_config)

    def test_get_task_config_success(self, tmp_path):
        """Test get_task_config successfully reads config"""
        config_file = tmp_path / "TestConfig.json"
        config_file.write_text('{"Name": "TestConfig", "EnabledTasks": [true, false]}')

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        result = get_task_config("TestConfig", mock_config)

        assert result["Name"] == "TestConfig"
        assert result["EnabledTasks"][0] is True

    def test_update_task_config_success(self, tmp_path):
        """Test update_task_config successfully updates config"""
        config_file = tmp_path / "TestConfig.json"
        config_file.write_text('{"Name": "TestConfig", "EnabledTasks": [false, false, false, false, false]}')

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        result = update_task_config("TestConfig", {"启用清体力": "是"}, mock_config)

        assert result["EnabledTasks"][1] is True

    def test_update_task_config_invalid_field(self, tmp_path):
        """Test update_task_config raises error for invalid field"""
        config_file = tmp_path / "TestConfig.json"
        config_file.write_text('{"Name": "TestConfig"}')

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with pytest.raises(InvalidTaskFieldError):
            update_task_config("TestConfig", {"不存在的字段": "值"}, mock_config)

    def test_list_task_configs(self, tmp_path):
        """Test list_task_configs returns config names"""
        (tmp_path / "Default.json").write_text('{"Name": "Default"}')
        (tmp_path / "MyConfig.json").write_text('{"Name": "MyConfig"}')

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        result = list_task_configs(mock_config)

        assert "Default" in result
        assert "MyConfig" in result

    def test_list_task_configs_empty_dir(self, tmp_path):
        """Test list_task_configs returns empty list when dir is empty"""
        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        result = list_task_configs(mock_config)

        assert result == []


class TestTaskConfigFields:
    """Tests for TASK_CONFIG_FIELDS completeness"""

    def test_all_task_names_present(self):
        """Verify key task-related field names are in mappings"""
        expected_fields = [
            "启用启动游戏", "启用清体力", "启用领取奖励", "启用旷宇纷争", "启用任务结束",
            "启用差分宇宙", "启用货币战争",
            "货币战争模式", "货币战争难度", "货币战争运行次数",
            "启用补充体力", "补充体力次数",
            "领取每日实训", "领取无名勋礼", "领取邮件奖励",
            "任务后退出游戏", "任务后关机",
        ]

        for field in expected_fields:
            assert field in TASK_CONFIG_FIELDS, f"Missing field: {field}"
