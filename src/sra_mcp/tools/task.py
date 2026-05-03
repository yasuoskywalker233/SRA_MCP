"""MCP tools for SRA task operations"""
from typing import Optional
from sra_mcp.config import SRAConfig
from sra_mcp.sra_controller import (
    SRAController,
    SRAProcessError,
    SRAAlreadyRunningError,
    SRATimeoutError,
    SRAConfigNotFoundError,
)


class TaskToolError(Exception):
    """Base exception for task operations"""
    pass

# 启动SRA GUI
def start_sra(config: Optional[SRAConfig] = None) -> dict:
    """Start SRA GUI application."""
    if config is None:
        config = SRAConfig.load()

    controller = SRAController(config.sra_path)

    try:
        controller.start_gui()
        return {"success": True, "message": "SRA started successfully"}
    except SRAAlreadyRunningError:
        return {"success": False, "message": "SRA is already running"}
    except SRAProcessError as e:
        return {"success": False, "message": str(e)}


def run_task(
    config_name: str,
    task_name: Optional[str] = None,
    timeout: int = 1800,
    sra_config: Optional[SRAConfig] = None,
    admin: bool = False
) -> dict:
    """Run an SRA task synchronously."""
    if sra_config is None:
        sra_config = SRAConfig.load()

    controller = SRAController(sra_config.sra_path)

    # Validate config exists
    configs_dir = sra_config.get_configs_dir()
    config_file = configs_dir / f"{config_name}.json"
    if not config_file.exists():
        raise SRAConfigNotFoundError(f"Config '{config_name}' not found at {config_file}")

    try:
        result = controller.run_task(
            config_name=config_name,
            task_name=task_name,
            timeout=timeout,
            admin=admin
        )

        return {
            "success": result.success,
            "message": result.message,
            "output": result.output,
        }

    except SRATimeoutError as e:
        return {
            "success": False,
            "message": f"Task timed out: {e}",
            "output": "",
        }
    except SRAProcessError as e:
        return {
            "success": False,
            "message": f"Task execution failed: {e}",
            "output": "",
        }