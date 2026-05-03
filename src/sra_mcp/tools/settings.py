"""MCP tools for SRA settings management"""
import json
import os
from pathlib import Path
from typing import Optional
from sra_mcp.config import SRAConfig
from sra_mcp.mappings import SETTINGS_FIELDS, JsonToDisplayMapper, DisplayToJsonMapper


class SettingsError(Exception):
    """Base exception for settings operations"""
    pass


class SettingsReadError(SettingsError):
    """Raised when settings cannot be read"""
    pass


class SettingsWriteError(SettingsError):
    """Raised when settings cannot be written"""
    pass


class InvalidFieldError(SettingsError):
    """Raised when an invalid field name or value is provided"""
    pass


def _get_settings_path() -> Path:
    """Get the path to settings.json"""
    appdata = Path(os.environ.get("APPDATA", ""))
    return appdata / "SRA" / "settings.json"


def get_settings() -> dict:
    """Read raw SRA settings JSON."""
    settings_path = _get_settings_path()
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SettingsReadError(f"Settings file not found at {settings_path}")
    except json.JSONDecodeError as e:
        raise SettingsReadError(f"Invalid JSON in settings file: {e}")


def get_settings_readable() -> dict:
    """Read SRA settings with human-readable field names and values."""
    raw = get_settings()
    mapper = JsonToDisplayMapper()
    readable = mapper.map(raw)
    return {
        "raw": raw,
        "readable": readable,
    }


def update_settings(updates: dict, config: Optional[SRAConfig] = None) -> dict:
    """Update SRA settings with human-readable field names and values."""
    settings_path = _get_settings_path()

    # Load current settings
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            current = json.load(f)
    except FileNotFoundError:
        raise SettingsReadError(f"Settings file not found at {settings_path}")
    except json.JSONDecodeError as e:
        raise SettingsReadError(f"Invalid JSON in settings file: {e}")

    # Validate all fields first
    mapper = DisplayToJsonMapper()
    validated = mapper.map(updates)

    # Check for invalid fields
    invalid_fields = set(updates.keys()) - set(SETTINGS_FIELDS.keys())
    if invalid_fields:
        raise InvalidFieldError(f"Unknown fields: {invalid_fields}")

    # Apply updates
    current.update(validated)

    # Write back
    try:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise SettingsWriteError(f"Failed to write settings: {e}")

    return current