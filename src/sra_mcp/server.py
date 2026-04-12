"""SRA MCP Server - main entry point"""
import sys
from mcp.server.fastmcp import FastMCP

from sra_mcp.config import SRAConfig, ConfigNotFoundError, ConfigReadError
from sra_mcp.tools.settings import (
    get_settings,
    get_settings_readable,
    update_settings,
    SettingsReadError,
    SettingsWriteError,
    InvalidFieldError,
)
from sra_mcp.tools.task import (
    start_sra,
    run_task,
    TaskToolError,
)
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
from sra_mcp.sra_controller import (
    SRAProcessError,
    SRAConfigNotFoundError,
)


# Create FastMCP server
mcp = FastMCP("sra-mcp")

# Global config instance
_config: SRAConfig | None = None


def get_config() -> SRAConfig:
    """Get or load the global config instance"""
    global _config
    if _config is None:
        _config = SRAConfig.load()
    return _config


@mcp.tool()
def sra_get_settings() -> dict:
    """Get raw SRA settings JSON."""
    try:
        return get_settings(get_config())
    except (ConfigNotFoundError, ConfigReadError, SettingsReadError) as e:
        raise Exception(f"Failed to read settings: {e}")


@mcp.tool()
def sra_get_settings_readable() -> dict:
    """Get SRA settings with human-readable field names and values."""
    try:
        return get_settings_readable(get_config())
    except (ConfigNotFoundError, ConfigReadError, SettingsReadError) as e:
        raise Exception(f"Failed to read settings: {e}")


@mcp.tool()
def sra_update_settings(settings: dict) -> dict:
    """
    Update SRA settings with human-readable field names and values.

    Args:
        settings: Dictionary of {显示名称: 值} to update
                  e.g., {"语言": "English", "更新通道": "测试版"}
    """
    try:
        return update_settings(settings, get_config())
    except (ConfigNotFoundError, ConfigReadError) as e:
        raise Exception(f"Config error: {e}")
    except (SettingsReadError, SettingsWriteError) as e:
        raise Exception(f"Failed to update settings: {e}")
    except InvalidFieldError as e:
        raise Exception(f"Invalid field: {e}")


@mcp.tool()
def sra_start() -> dict:
    """Start SRA GUI application."""
    try:
        return start_sra(get_config())
    except ConfigNotFoundError as e:
        raise Exception(f"Config not found: {e}")
    except SRAProcessError as e:
        raise Exception(f"Failed to start SRA: {e}")


@mcp.tool()
def sra_list_configs() -> list[str]:
    """
    List all available task config names.

    Returns:
        List of config names (e.g., ["Default", "MyConfig"])
    """
    try:
        return list_task_configs(get_config())
    except ConfigNotFoundError as e:
        raise Exception(f"Config not found: {e}")


@mcp.tool()
def sra_get_config(config_name: str) -> dict:
    """
    Get raw SRA task config JSON.

    Args:
        config_name: Name of the config (e.g., "Default")
    """
    try:
        return get_task_config(config_name, get_config())
    except (ConfigNotFoundError, TaskConfigNotFoundError, TaskConfigReadError) as e:
        raise Exception(f"Failed to read config: {e}")


@mcp.tool()
def sra_get_config_readable(config_name: str) -> dict:
    """
    Get SRA task config with human-readable field names and values.

    Args:
        config_name: Name of the config (e.g., "Default")
    """
    try:
        return get_task_config_readable(config_name, get_config())
    except (ConfigNotFoundError, TaskConfigNotFoundError, TaskConfigReadError) as e:
        raise Exception(f"Failed to read config: {e}")


@mcp.tool()
def sra_update_config(config_name: str, updates: dict) -> dict:
    """
    Update SRA task config with human-readable field names and values.

    Args:
        config_name: Name of the config to update
        updates: Dictionary of {显示名称: 值} to update
                 e.g., {"启用清体力": "是", "补充体力次数": 3}
    """
    try:
        return update_task_config(config_name, updates, get_config())
    except (ConfigNotFoundError, TaskConfigNotFoundError) as e:
        raise Exception(f"Config not found: {e}")
    except TaskConfigReadError as e:
        raise Exception(f"Failed to read config: {e}")
    except TaskConfigWriteError as e:
        raise Exception(f"Failed to update config: {e}")
    except InvalidTaskFieldError as e:
        raise Exception(f"Invalid field: {e}")


@mcp.tool()
def sra_run_task(
    config_name: str,
    task_name: str | None = None,
    timeout: int = 1800
) -> dict:
    """
    Run an SRA task synchronously.

    Args:
        config_name: Name of the config to use (e.g., "Default")
        task_name: Optional specific task name (e.g., "StartGameTask")
        timeout: Timeout in seconds (default 1800 = 30 minutes)
    """
    try:
        return run_task(
            config_name=config_name,
            task_name=task_name,
            timeout=timeout,
            sra_config=get_config(),
            admin=True  # Start SRA with admin privileges if needed
        )
    except ConfigNotFoundError as e:
        raise Exception(f"Config not found: {e}")
    except SRAConfigNotFoundError as e:
        raise Exception(f"Config not found: {e}")
    except (TaskToolError, SRAProcessError) as e:
        raise Exception(f"Task execution failed: {e}")


def main():
    """Main entry point"""
    # Load config on startup to catch errors early
    try:
        get_config()
    except ConfigNotFoundError as e:
        print(f"Warning: {e}", file=sys.stderr)
    except ConfigReadError as e:
        print(f"Warning: {e}", file=sys.stderr)

    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
