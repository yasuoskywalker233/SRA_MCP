# SRA MCP Server

MCP server for controlling StarRailAssistant (SRA) via Model Context Protocol.

## Features

- Read SRA settings (raw JSON or human-readable format)
- Update SRA settings using display names
- Read SRA task configs (raw JSON or human-readable format)
- Update SRA task configs using display names
- List available task configs
- Start SRA GUI
- Run SRA tasks synchronously

## Installation

```bash
pip install -e .
```

## Configuration

Create `config.json` in the MCP directory:

```json
{
  "sra_path": "D:\\Software\\StarRailAssistant"
}
```

## MCP Client Configuration

Add to your MCP settings:

```json
{
  "sra-mcp": {
    "command": "python",
    "args": ["-m", "sra_mcp"],
    "cwd": "SRA_MCP"
  }
}
```

## Available Tools

### Settings Tools
| Tool | Description |
|------|-------------|
| `sra_get_settings` | Get raw settings JSON |
| `sra_get_settings_readable` | Get settings with human-readable field names |
| `sra_update_settings` | Update settings using display names |

### Task Config Tools
| Tool | Description |
|------|-------------|
| `sra_list_configs` | List all available task config names |
| `sra_get_config` | Get raw task config JSON |
| `sra_get_config_readable` | Get task config with human-readable field names |
| `sra_update_config` | Update task config using display names |

### Task Execution Tools
| Tool | Description |
|------|-------------|
| `sra_start` | Start SRA GUI |
| `sra_run_task` | Run a task with optional timeout |

## Usage Examples

### Get Settings
```
sra_get_settings() -> {"language": 0, "appChannel": 0, ...}
```

### Get Readable Settings
```
sra_get_settings_readable() -> {
  "raw": {...},
  "readable": {
    "语言": {"value": 0, "display": "简体中文", "options": ["简体中文", "English"]},
    ...
  }
}
```

### Update Settings
```
sra_update_settings({"语言": "English", "启用叠加层": "是"})
```

### List Task Configs
```
sra_list_configs() -> ["Default", "MyConfig"]
```

### Get Task Config
```
sra_get_config("Default") -> {"name": "Default", "enabledTasks": [true, false, ...], ...}
```

### Get Readable Task Config
```
sra_get_config_readable("Default") -> {
  "raw": {...},
  "readable": {
    "启用启动游戏": {"value": true, "display": "是", "options": ["否", "是"]},
    "启用清体力": {"value": false, "display": "否", "options": ["否", "是"]},
    "游戏通道": {"value": 0, "display": "国服", "options": ["国服", "B服"]},
    "启用差分宇宙": {"value": true, "display": "是", "options": ["否", "是"]},
    "启用货币战争": {"value": false, "display": "否", "options": ["否", "是"]},
    "货币战争模式": {"value": 0, "display": "标准博弈", "options": ["标准博弈", "超频博弈", "刷开局"]},
    "任务后退出游戏": {"value": false, "display": "否", "options": ["否", "是"]},
    ...
  }
}
```

### Update Task Config
```
# Enable trailblaze power task and set replenish times
sra_update_config("Default", {
  "启用清体力": "是",
  "补充体力次数": 3,
  "启用差分宇宙": "是",
  "差分宇宙运行次数": 5,
  "货币战争模式": "标准博弈"
})
```

### Start SRA
```
sra_start() -> {"success": true, "message": "SRA started successfully"}
```

### Run Task
```
sra_run_task("Default")  # Run all enabled tasks in Default config
sra_run_task("Default", "StartGameTask")  # Run specific task
sra_run_task("Default", timeout=3600)  # 1 hour timeout
```

## Limitations

- Windows only (SRA itself is Windows-only)
- Requires .NET 8.0 to run SRA GUI
- Task execution is synchronous with configurable timeout (default 30 minutes)
