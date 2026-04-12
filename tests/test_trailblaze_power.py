"""Tests for TrailblazePowerTaskList tools"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from sra_mcp.tools.trailblaze_power import (
    VALID_OPERATIONS,
    VALID_FIELDS,
    validate_task_fields,
    InvalidTaskIdError,
    InvalidLevelError,
    CountExceedsMaxError,
    TypeValidationError,
)


class TestValidateTaskFields:
    """Tests for validate_task_fields function"""

    def test_valid_add_operation(self):
        """Test validation passes for valid add operation"""
        task_config = {
            "calyx_crimson": {
                "name": "拟造花萼（赤）",
                "max_count": 24,
                "max_level": 17,
            }
        }
        task_data = {
            "Name": "拟造花萼（赤）",
            "Id": "calyx_crimson",
            "Level": 10,
            "Count": 2,
            "RunTimes": 1,
            "AutoDetect": True,
        }
        errors = validate_task_fields(task_data, task_config)
        assert errors == []

    def test_invalid_task_id(self):
        """Test validation fails for invalid task ID"""
        task_config = {
            "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
        }
        task_data = {"Id": "invalid_id", "Level": 1}
        errors = validate_task_fields(task_data, task_config)
        assert len(errors) > 0
        assert "无效任务 ID" in errors[0]

    def test_level_out_of_range(self):
        """Test validation fails when level exceeds max"""
        task_config = {
            "echo_of_war": {"name": "历战余响", "max_count": 3, "max_level": 8}
        }
        task_data = {"Id": "echo_of_war", "Level": 15}
        errors = validate_task_fields(task_data, task_config)
        assert len(errors) > 0
        assert "Level 必须为 1-8" in errors[0]

    def test_count_exceeds_max(self):
        """Test validation fails when count exceeds max_count"""
        task_config = {
            "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
        }
        task_data = {"Id": "calyx_crimson", "Level": 1, "Count": 30}
        errors = validate_task_fields(task_data, task_config)
        assert len(errors) > 0
        assert "Count 不能超过 24" in errors[0]

    def test_type_validation_errors(self):
        """Test validation fails for wrong field types"""
        task_config = {
            "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
        }
        task_data = {"Id": "calyx_crimson", "Level": "ten"}  # should be int
        errors = validate_task_fields(task_data, task_config)
        assert len(errors) > 0
        assert "Level 必须为整数" in errors[0]

    def test_partial_update(self):
        """Test validation passes for partial update (only Level)"""
        task_config = {
            "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
        }
        task_data = {"Level": 15}
        errors = validate_task_fields(task_data, task_config, allow_partial=True, is_update=True)
        assert errors == []

    def test_negative_level(self):
        """Test validation fails for negative level"""
        task_config = {
            "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
        }
        task_data = {"Level": -1}
        errors = validate_task_fields(task_data, task_config)
        assert len(errors) > 0
        assert "正整数" in errors[0]


class TestConstants:
    """Tests for constants"""

    def test_valid_operations(self):
        """Test VALID_OPERATIONS contains expected values"""
        assert VALID_OPERATIONS == {"add", "update", "remove"}

    def test_valid_fields(self):
        """Test VALID_FIELDS contains expected values"""
        expected = {"Name", "Id", "Level", "LevelName", "Count", "RunTimes", "AutoDetect"}
        assert VALID_FIELDS == expected


class TestGetTrailblazePowerTaskList:
    """Tests for get_trailblaze_power_task_list function"""

    def test_get_task_list_success(self, tmp_path):
        """Test successfully getting task list from config"""
        from sra_mcp.tools.trailblaze_power import get_trailblaze_power_task_list

        # Mock config
        config_file = tmp_path / "TestConfig.json"
        config_file.write_text(json.dumps({
            "Name": "TestConfig",
            "TrailblazePowerTaskList": [
                {"Name": "Task1", "Id": "calyx_crimson", "Level": 5}
            ]
        }))

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with patch("sra_mcp.tools.trailblaze_power.load_trailblaze_power_config") as mock_load:
            mock_load.return_value = {
                "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
            }

            result = get_trailblaze_power_task_list("TestConfig", mock_config)

            assert result["config_name"] == "TestConfig"
            assert len(result["task_list"]) == 1
            assert result["task_list"][0]["Name"] == "Task1"
            assert len(result["available_tasks"]) == 1


class TestUpdateTrailblazePowerTaskList:
    """Tests for update_trailblaze_power_task_list function"""

    def test_add_task_success(self, tmp_path):
        """Test successfully adding a task"""
        from sra_mcp.tools.trailblaze_power import update_trailblaze_power_task_list

        config_file = tmp_path / "TestConfig.json"
        config_file.write_text(json.dumps({
            "Name": "TestConfig",
            "TrailblazePowerTaskList": []
        }))

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with patch("sra_mcp.tools.trailblaze_power.load_trailblaze_power_config") as mock_load:
            mock_load.return_value = {
                "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
            }
            with patch("sra_mcp.tools.trailblaze_power.validate_task_fields") as mock_validate:
                mock_validate.return_value = []  # No validation errors

                result = update_trailblaze_power_task_list("TestConfig", {
                    "action": "add",
                    "Name": "拟造花萼（赤）",
                    "Id": "calyx_crimson",
                    "Level": 10
                }, mock_config)

                assert result["success"] is True
                assert "已添加关卡" in result["message"]
                assert len(result["data"]["trailblaze_power_task_list"]) == 1

    def test_update_task_success(self, tmp_path):
        """Test successfully updating a task"""
        from sra_mcp.tools.trailblaze_power import update_trailblaze_power_task_list

        config_file = tmp_path / "TestConfig.json"
        config_file.write_text(json.dumps({
            "Name": "TestConfig",
            "TrailblazePowerTaskList": [
                {"Name": "Task1", "Id": "calyx_crimson", "Level": 5}
            ]
        }))

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with patch("sra_mcp.tools.trailblaze_power.load_trailblaze_power_config") as mock_load:
            mock_load.return_value = {
                "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
            }

            result = update_trailblaze_power_task_list("TestConfig", {
                "action": "update",
                "index": 0,
                "Level": 15
            }, mock_config)

            assert result["success"] is True
            assert result["data"]["trailblaze_power_task_list"][0]["Level"] == 15

    def test_remove_task_success(self, tmp_path):
        """Test successfully removing a task"""
        from sra_mcp.tools.trailblaze_power import update_trailblaze_power_task_list

        config_file = tmp_path / "TestConfig.json"
        config_file.write_text(json.dumps({
            "Name": "TestConfig",
            "TrailblazePowerTaskList": [
                {"Name": "Task1", "Id": "calyx_crimson", "Level": 5},
                {"Name": "Task2", "Id": "echo_of_war", "Level": 3}
            ]
        }))

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with patch("sra_mcp.tools.trailblaze_power.load_trailblaze_power_config") as mock_load:
            mock_load.return_value = {
                "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17},
                "echo_of_war": {"name": "历战余响", "max_count": 3, "max_level": 8}
            }

            result = update_trailblaze_power_task_list("TestConfig", {
                "action": "remove",
                "index": 0
            }, mock_config)

            assert result["success"] is True
            assert "已删除关卡" in result["message"]
            assert len(result["data"]["trailblaze_power_task_list"]) == 1
            assert result["data"]["trailblaze_power_task_list"][0]["Name"] == "Task2"

    def test_invalid_action_raises_error(self, tmp_path):
        """Test that invalid action raises InvalidOperationError"""
        from sra_mcp.tools.trailblaze_power import update_trailblaze_power_task_list, InvalidOperationError

        config_file = tmp_path / "TestConfig.json"
        config_file.write_text(json.dumps({
            "Name": "TestConfig",
            "TrailblazePowerTaskList": []
        }))

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with patch("sra_mcp.tools.trailblaze_power.load_trailblaze_power_config") as mock_load:
            mock_load.return_value = {
                "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
            }
            with pytest.raises(InvalidOperationError):
                update_trailblaze_power_task_list("TestConfig", {
                    "action": "invalid_action"
                }, mock_config)

    def test_index_out_of_range_raises_error(self, tmp_path):
        """Test that out of range index raises IndexOutOfRangeError"""
        from sra_mcp.tools.trailblaze_power import update_trailblaze_power_task_list, IndexOutOfRangeError

        config_file = tmp_path / "TestConfig.json"
        config_file.write_text(json.dumps({
            "Name": "TestConfig",
            "TrailblazePowerTaskList": [
                {"Name": "Task1", "Id": "calyx_crimson", "Level": 5}
            ]
        }))

        mock_config = MagicMock()
        mock_config.get_configs_dir.return_value = tmp_path

        with patch("sra_mcp.tools.trailblaze_power.load_trailblaze_power_config") as mock_load:
            mock_load.return_value = {
                "calyx_crimson": {"name": "拟造花萼（赤）", "max_count": 24, "max_level": 17}
            }

            with pytest.raises(IndexOutOfRangeError):
                update_trailblaze_power_task_list("TestConfig", {
                    "action": "update",
                    "index": 10
                }, mock_config)