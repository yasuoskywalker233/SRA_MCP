"""MCP tools for SRA task configuration management."""
import json
from pathlib import Path
from typing import Optional
from sra_mcp.config import SRAConfig, ConfigNotFoundError, ConfigReadError
from sra_mcp.task_config_mappings import (
    TASK_CONFIG_FIELDS,
    TaskConfigJsonToDisplayMapper,
    TaskConfigDisplayToJsonMapper,
)


class TaskConfigError(Exception):
    """Base exception for task config operations"""
    pass


class TaskConfigNotFoundError(TaskConfigError):
    """Raised when task config file is not found"""
    pass


class TaskConfigReadError(TaskConfigError):
    """Raised when task config cannot be read"""
    pass


class TaskConfigWriteError(TaskConfigError):
    """Raised when task config cannot be written"""
    pass


class InvalidTaskFieldError(TaskConfigError):
    """Raised when an invalid field name is provided"""
    pass


def _get_config_path(config_name: str, config: Optional[SRAConfig] = None) -> Path:
    """Get the path to a task config JSON file."""
    if config is None:
        config = SRAConfig.load()

    configs_dir = config.get_configs_dir()
    return configs_dir / f"{config_name}.json"


def get_task_config(config_name: str, config: Optional[SRAConfig] = None) -> dict:
    """
    Read raw SRA task config JSON.

    Args:
        config_name: Name of the config (e.g., "Default")
        config: Optional SRAConfig instance

    Returns:
        The complete task config JSON content as a dictionary
    """
    config_path = _get_config_path(config_name, config)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise TaskConfigNotFoundError(f"Task config '{config_name}' not found at {config_path}")
    except json.JSONDecodeError as e:
        raise TaskConfigReadError(f"Invalid JSON in task config file: {e}")


def get_task_config_readable(config_name: str, config: Optional[SRAConfig] = None) -> dict:
    """
    Read SRA task config with human-readable field names and values.

    Args:
        config_name: Name of the config (e.g., "Default")
        config: Optional SRAConfig instance

    Returns:
        {
            "raw": { ... },  # Original JSON
            "readable": {
                "启用清体力": { "value": True, "display": "是", "options": [...] },
                ...
            }
        }
    """
    raw = get_task_config(config_name, config)
    mapper = TaskConfigJsonToDisplayMapper()
    readable = mapper.map(raw)

    return {
        "raw": raw,
        "readable": readable,
    }


def update_task_config(
    config_name: str,
    updates: dict,
    config: Optional[SRAConfig] = None
) -> dict:
    """
    Update SRA task config with human-readable field names and values.

    Args:
        config_name: Name of the config to update
        updates: Dictionary of {显示名称: 值} to update
        config: Optional SRAConfig instance

    Returns:
        Updated task config JSON content
    """
    config_path = _get_config_path(config_name, config)

    # Load current config
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            current = json.load(f)
    except FileNotFoundError:
        raise TaskConfigNotFoundError(f"Task config '{config_name}' not found at {config_path}")
    except json.JSONDecodeError as e:
        raise TaskConfigReadError(f"Invalid JSON in task config file: {e}")

    # Validate all fields first
    mapper = TaskConfigDisplayToJsonMapper()
    validated = mapper.map(updates)

    # Check for invalid fields
    invalid_fields = set(updates.keys()) - set(TASK_CONFIG_FIELDS.keys())
    if invalid_fields:
        raise InvalidTaskFieldError(f"Unknown fields: {invalid_fields}")

    # Apply updates (merge with current)
    current.update(validated)

    # Write back
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise TaskConfigWriteError(f"Failed to write task config: {e}")

    return current


def list_task_configs(config: Optional[SRAConfig] = None) -> list[str]:
    """
    List all available task config names.

    Args:
        config: Optional SRAConfig instance

    Returns:
        List of config names (without .json extension)
    """
    if config is None:
        config = SRAConfig.load()

    configs_dir = config.get_configs_dir()

    if not configs_dir.exists():
        return []

    return [p.stem for p in configs_dir.glob("*.json")]
