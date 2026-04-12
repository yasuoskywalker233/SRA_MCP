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
- Manage TrailblazePowerTaskList (add, update, remove tasks)

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

### TrailblazePowerTaskList Tools
| Tool | Description |
|------|-------------|
| `sra_get_trailblaze_power_task_list` | Get TrailblazePowerTaskList details and available tasks |
| `sra_update_trailblaze_power_task_list` | Add, update, or remove tasks in TrailblazePowerTaskList |

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

### Get TrailblazePowerTaskList
```
sra_get_trailblaze_power_task_list("Daily") -> {
  "config_name": "Daily",
  "task_list": [
    {"Name": "拟造花萼（赤）", "Id": "calyx_crimson", "Level": 17, ...},
    {"Name": "历战余响", "Id": "echo_of_war", "Level": 1, ...}
  ],
  "available_tasks": [
    {"id": "calyx_crimson", "name": "拟造花萼（赤）", "max_level": 17, "max_count": 24},
    {"id": "echo_of_war", "name": "历战余响", "max_level": 8, "max_count": 3},
    ...
  ]
}
```

### Add TrailblazePowerTask
```
sra_update_trailblaze_power_task_list("Daily", {
  "action": "add",
  "Name": "历战余响",
  "Id": "echo_of_war",
  "Level": 3
})
```

### Update TrailblazePowerTask
```
sra_update_trailblaze_power_task_list("Daily", {
  "action": "update",
  "index": 0,
  "Level": 8
})
```

### Remove TrailblazePowerTask
```
sra_update_trailblaze_power_task_list("Daily", {
  "action": "remove",
  "index": 1
})
```

## TrailblazePowerTaskList Fields

### Task Item Structure
| Field | Type | Description |
|-------|------|-------------|
| `Name` | string | Display name of the task |
| `Id` | string | Task identifier (e.g., `calyx_crimson`, `echo_of_war`) |
| `Level` | int | Level number (must be within valid range) |
| `LevelName` | string | Level display name (auto-synced from Level, do not set manually) |
| `Count` | int | Stamina cost per run (max varies by task) |
| `RunTimes` | int | Number of times to execute |
| `AutoDetect` | bool | Auto-detect level or manual |

### LevelName Auto-Sync

When `Level` is modified, `LevelName` is automatically updated based on the frontend level data. You do not need to specify `LevelName` manually when adding or updating tasks.

### Available Task Levels

Use `sra_get_trailblaze_power_task_list` to get the full list of available levels for each task:

```json
{
  "available_tasks": [
    {
      "id": "calyx_crimson",
      "name": "拟造花萼（赤）",
      "max_level": 17,
      "max_count": 24,
      "frontend_levels": [
        "---选择副本---",
        "月狂獠牙（毁灭）",
        "净世残刃（毀灭）",
        ...
        "《绒绒号》典藏版合集（欢愉）"
      ]
    }
  ]
}
```

### Valid Task IDs
| ID | Name | Max Level | Max Count |
|----|------|-----------|-----------|
| `ornament_extraction` | 饰品提取 | 13 | 6 |
| `calyx_golden` | 拟造花萼（金） | 15 | 24 |
| `calyx_crimson` | 拟造花萼（赤） | 17 | 24 |
| `stagnant_shadow` | 凝滞虚影 | 28 | 8 |
| `caver_of_corrosion` | 侵蚀隧洞 | 15 | 6 |
| `echo_of_war` | 历战余响 | 8 | 3 | |

## Limitations

- Windows only (SRA itself is Windows-only)
- Requires .NET 8.0 to run SRA GUI
- Task execution is synchronous with configurable timeout (default 30 minutes)
