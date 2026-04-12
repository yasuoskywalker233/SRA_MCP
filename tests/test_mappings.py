"""Tests for mappings.py"""
import pytest
from src.sra_mcp.mappings import SETTINGS_FIELDS, JsonToDisplayMapper, DisplayToJsonMapper


class TestSettingsFields:
    def test_settings_fields_contains_language(self):
        """Verify language field exists"""
        assert "语言" in SETTINGS_FIELDS
        assert SETTINGS_FIELDS["语言"]["json_field"] == "language"
        assert SETTINGS_FIELDS["语言"]["options"] == ["简体中文", "English"]
        assert SETTINGS_FIELDS["语言"]["type"] == "int"


class TestJsonToDisplayMapper:
    def test_json_to_display_mapper_bool(self):
        """Verify boolean value mapping"""
        mapper = JsonToDisplayMapper()
        raw_settings = {
            "allowNotifications": True,
            "isOverlayEnabled": False,
        }
        result = mapper.map(raw_settings)

        assert result["允许通知"]["value"] is True
        assert result["允许通知"]["display"] == "是"
        assert result["启用叠加层"]["value"] is False
        assert result["启用叠加层"]["display"] == "否"

    def test_json_to_display_mapper_int_with_options(self):
        """Verify int mapping with options"""
        mapper = JsonToDisplayMapper()
        raw_settings = {
            "language": 0,  # 简体中文
            "appChannel": 1,  # 测试版
        }
        result = mapper.map(raw_settings)

        assert result["语言"]["value"] == 0
        assert result["语言"]["display"] == "简体中文"
        assert result["更新通道"]["value"] == 1
        assert result["更新通道"]["display"] == "测试版"

    def test_json_to_display_mapper_int_without_options(self):
        """Verify int mapping without options"""
        mapper = JsonToDisplayMapper()
        raw_settings = {
            "gamePathIndex": 2,
            "defaultPage": 1,
        }
        result = mapper.map(raw_settings)

        assert result["游戏路径索引"]["value"] == 2
        assert result["游戏路径索引"]["display"] == "2"
        assert result["默认页面"]["value"] == 1
        assert result["默认页面"]["display"] == "1"

    def test_json_to_display_mapper_float(self):
        """Verify float mapping"""
        mapper = JsonToDisplayMapper()
        raw_settings = {
            "confidenceThreshold": 0.85,
            "backgroundOpacity": 0.5,
        }
        result = mapper.map(raw_settings)

        assert result["识图置信度阈值"]["value"] == 0.85
        assert result["识图置信度阈值"]["display"] == "0.85"
        assert result["背景图不透明度"]["value"] == 0.5
        assert result["背景图不透明度"]["display"] == "0.5"

    def test_json_to_display_mapper_unknown_field(self):
        """Verify unknown fields are ignored"""
        mapper = JsonToDisplayMapper()
        raw_settings = {
            "unknownField": "value",
            "language": 0,
        }
        result = mapper.map(raw_settings)

        assert "unknownField" not in result
        assert "语言" in result


class TestDisplayToJsonMapper:
    def test_display_to_json_mapper_bool(self):
        """Verify reverse boolean mapping"""
        mapper = DisplayToJsonMapper()
        display_settings = {
            "允许通知": "是",
            "启用叠加层": "否",
        }
        result = mapper.map(display_settings)

        assert result["allowNotifications"] is True
        assert result["isOverlayEnabled"] is False

    def test_display_to_json_mapper_int(self):
        """Verify reverse int mapping"""
        mapper = DisplayToJsonMapper()
        display_settings = {
            "语言": "English",
            "更新通道": "测试版",
        }
        result = mapper.map(display_settings)

        assert result["language"] == 1  # English is index 1
        assert result["appChannel"] == 1  # 测试版 is index 1

    def test_display_to_json_mapper_unknown_field(self):
        """Verify unknown fields are ignored"""
        mapper = DisplayToJsonMapper()
        display_settings = {
            "未知字段": "值",
            "语言": "简体中文",
        }
        result = mapper.map(display_settings)

        assert "未知字段" not in result
        assert result["language"] == 0
