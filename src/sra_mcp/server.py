"""SRA MCP Server - main entry point"""
import argparse
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
from sra_mcp.tools.trailblaze_power import (
    get_trailblaze_power_task_list,
    update_trailblaze_power_task_list,
    FRONTEND_TASKSNAME_TASKID,
    FRONTEND_LEVELS,
    TrailblazePowerError,
    TrailblazePowerReadError,
    InvalidOperationError,
    IndexOutOfRangeError,
    InvalidTaskIdError,
    InvalidLevelError,
    CountExceedsMaxError,
    TypeValidationError,
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


# 先不用更新设置了
# @mcp.tool()
# def sra_get_settings() -> dict:
#     """Get raw SRA settings JSON."""
#     try:
#         return get_settings(get_config())
#     except (ConfigNotFoundError, ConfigReadError, SettingsReadError) as e:
#         raise Exception(f"Failed to read settings: {e}")


# @mcp.tool()
# def sra_get_settings_readable() -> dict:
#     """Get SRA settings with human-readable field names and values."""
#     try:
#         return get_settings_readable(get_config())
#     except (ConfigNotFoundError, ConfigReadError, SettingsReadError) as e:
#         raise Exception(f"Failed to read settings: {e}")


# @mcp.tool()
# def sra_update_settings(settings: dict) -> dict:
#     """
#     Update SRA settings with human-readable field names and values.

#     Args:
#         settings: Dictionary of {显示名称: 值} to update
#                   e.g., {"语言": "English", "更新通道": "测试版"}
#     """
#     try:
#         return update_settings(settings, get_config())
#     except (ConfigNotFoundError, ConfigReadError) as e:
#         raise Exception(f"Config error: {e}")
#     except (SettingsReadError, SettingsWriteError) as e:
#         raise Exception(f"Failed to update settings: {e}")
#     except InvalidFieldError as e:
#         raise Exception(f"Invalid field: {e}")

# 启动SRA GUI MCP工具
@mcp.tool()
def sra_start() -> dict:
    """Start SRA GUI application."""
    try:
        return start_sra(get_config())
    except ConfigNotFoundError as e:
        raise Exception(f"Config not found: {e}")
    except SRAProcessError as e:
        raise Exception(f"Failed to start SRA: {e}")

# 列出所有配置
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

# 获取某个配置 以Json格式
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

# 获取某个配置,以可读模式
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

# 更新目标配置的配置项
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


# 运行目标配置，超时时间默认为3600秒
@mcp.tool()
def sra_run_task(
    config_name: str,
    task_name: str | None = None,
    timeout: int = 3600
) -> dict:
    """
    Run an SRA task synchronously.

    Args:
        config_name: Name of the config to use (e.g., "Default")
        task_name: Optional specific task name (e.g., "StartGameTask")
        timeout: Timeout in seconds (default 3600 = 60 minutes)
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

# 获取清体力任务列表的详细信息。
@mcp.tool()
def sra_get_trailblaze_power_task_list(config_name: str) -> dict:
    """
    获取清体力任务列表的详细信息。

    Args:
        config_name: 配置名称，如 "Daily"

    Returns:
        {
            "config_name": "Daily",
            "task_list": [...],
            "available_tasks": [...]
        }
    """
    try:
        return get_trailblaze_power_task_list(config_name, get_config())
    except TrailblazePowerReadError as e:
        raise Exception(f"读取清体力任务配置失败: {e}")

# 更新清体力任务列表
@mcp.tool()
def sra_update_trailblaze_power_task_list(config_name: str, operation: dict) -> dict:
    """
    对清体力任务列表进行原子操作（添加、修改、删除关卡）。

    Args:
        config_name: 配置名称，如 "Daily"
        operation: 操作对象，包含:
            - action: "add" | "update" | "remove"
            - index: 索引（update/remove 时必需）
            - Id: 任务ID，如 "calyx_crimson"
            - Name: 任务名称。如果传入任务名称但没有Id，会自动补全Id(add和update时，Id和Name至少要填写一个)
            - Level: 等级
            - LevelName: 等级名称，如果传入等级名称但没有Level，会自动补全Level(add和update时，Level和LevelName至少要填写一个)
            - Count: 体力消耗次数
            - RunTimes: 运行次数
            - AutoDetect: 是否自动检测

    Returns:
        {
            "success": True,
            "message": "已添加关卡：xxx",
            "data": {"trailblaze_power_task_list": [...]}
        }
    """
    # 预处理
    # 检查合法性
    if operation["action"] == "add":
        if "Id" not in operation and "Name" not in operation:
            raise Exception(f"add时需要提供Id或Name")
        if "Level" not in operation and "LevelName" not in operation:
            raise Exception(f"add时需要提供Level或LevelName")
    if operation["action"] == "update":
        # 如果提供了 index，补全当前任务信息
        if "index" in operation:
            current_config = get_task_config(config_name, get_config())
            task_list = current_config.get("TrailblazePowerTaskList", [])
            idx = operation["index"]
            if 0 <= idx < len(task_list):
                current_task = task_list[idx]
                if "Id" not in operation:
                    operation["Id"] = current_task.get("Id")
                if "Level" not in operation and "LevelName" not in operation:
                    operation["Level"] = current_task.get("Level")
        # 补全后仍需验证
        if "Id" not in operation and "Name" not in operation:
            raise Exception(f"update时需要提供Id或Name")
        if "Level" not in operation and "LevelName" not in operation:
            raise Exception(f"update时需要提供Level或LevelName")
    if operation["action"] == "remove":
        if "index" not in operation:
            raise Exception(f"remove时需要提供index")
    
    # 处理Id
    task_name = operation.get("Name")
    if task_name and "Id" not in operation and task_name in FRONTEND_TASKSNAME_TASKID:
        task_id = FRONTEND_TASKSNAME_TASKID[task_name]
        operation["Id"] = task_id
    elif task_name and "Id" not in operation:
        raise Exception(f"无效的任务名称:{task_name}")
    # 处理关卡名称
    task_id = operation.get("Id")
    level_name = operation.get("LevelName")
    if level_name and "Level" not in operation and task_id in FRONTEND_LEVELS:
        levels = FRONTEND_LEVELS[task_id][1:]
        for i, name in enumerate(levels, start=1):
            if name == level_name:
                operation["Level"] = i
                break
    elif level_name and "Level" not in operation:
        raise Exception(f"无效的等级名称：{level_name}")
      
    try:
        return update_trailblaze_power_task_list(config_name, operation, get_config())
    except TrailblazePowerError as e:
        raise Exception(f"更新清体力任务配置失败: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="SRA MCP Server")
    parser.add_argument("-c", "--config", type=str, help="Path to config.json")
    args = parser.parse_args()

    global _config
    try:
        _config = SRAConfig.load(args.config) if args.config else get_config()
    except ConfigNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ConfigReadError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    mcp.run()


if __name__ == "__main__":
    main()
