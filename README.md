# SRA MCP Server

通过模型上下文协议（MCP）控制星穹铁道助手（StarRailAssistant, SRA）的 MCP 服务器。

本项目由AI负责编码，人类起到督战作用>_<

## 功能特性

- 读取/更新 SRA 设置（原始 JSON 或人类可读格式）
- 读取/更新任务配置（原始 JSON 或人类可读格式）
- 列出可用任务配置
- 启动 SRA GUI 应用程序
- 同步运行 SRA 任务
- **新增** 管理 TrailblazePowerTaskList（添加、修改、删除清体力任务）

## 安装

```bash
pip install .
```

## 配置

在 MCP 目录下创建 `config.json`：配置StarRailAssistant的路径

```json
{
  "sra_path": "D:\\Software\\StarRailAssistant" // StarRailAssistant的安装路径
}
```

## MCP 客户端配置

在 Claude Code 的settings.json中添加：

路径：**SRA_MCP的绝对路径**，例如”D:\Work\SRA_MCP“，或者**相对于ClaudeCode工作目录的路径**，例如”../SRA_MCP“

```json
{
  "mcpServers": {
    "SRA_MCP": {
      "command": "sra-mcp",
      "cwd": "路径"
    }
  }
}
```

## 可用工具

### 设置工具
| 工具 | 描述 |
|------|------|
| `sra_get_settings` | 获取原始 settings.json |
| `sra_get_settings_readable` | 获取可读的设置（中文显示名称） |
| `sra_update_settings` | 使用显示名称更新设置（中文） |

### 任务配置工具
| 工具 | 描述 |
|------|------|
| `sra_list_configs` | 列出所有任务配置 |
| `sra_get_config` | 获取原始任务配置 JSON |
| `sra_get_config_readable` | 获取可读格式的任务配置 |
| `sra_update_config` | 使用显示名称更新任务配置（中文） |

### 任务执行工具
| 工具 | 描述 |
|------|------|
| `sra_start` | 启动 SRA GUI 应用程序 |
| `sra_run_task` | 同步运行任务（支持超时设置） |

### 清体力任务列表工具
| 工具 | 描述 |
|------|------|
| `sra_get_trailblaze_power_task_list` | 获取清体力任务列表详情及可用关卡 |
| `sra_update_trailblaze_power_task_list` | 添加、修改或删除清体力任务（原子操作） |

## 使用示例

### 设置操作

```python
# 获取原始设置
sra_get_settings()

# 获取可读设置（中文字段名）
sra_get_settings_readable()

# 更新设置
sra_update_settings({"语言": "English", "StartStopHotkey": "f10"})
```

### 任务配置操作

```python
# 列出所有配置
sra_list_configs()

# 获取配置详情
sra_get_config("Daily")

# 更新任务配置（使用中文显示名称）
sra_update_config("Daily", {
    "启用清体力": "是",
    "补充体力次数": 3,
    "启用差分宇宙": "是"
})
```

### 任务执行

```python
# 运行配置中所有已启用的任务
sra_run_task("Daily")

# 运行指定任务
sra_run_task("Daily", "StartGameTask")

# 自定义超时时间（秒）
sra_run_task("Daily", timeout=3600)
```

### 清体力任务列表操作

```python
# 获取任务列表和可用关卡
sra_get_trailblaze_power_task_list("Daily")
# 返回: {config_name, task_list, available_tasks: [{id, name, max_level, max_count, frontend_levels}]}

# 添加任务（LevelName 根据 Level 自动填充）
sra_update_trailblaze_power_task_list("Daily", {
    "action": "add",
    "Name": "历战余响",
    "Id": "echo_of_war",
    "Level": 3
    # LevelName 自动填充为: "心兽的战场"
})

# 修改任务等级（LevelName 自动更新）
sra_update_trailblaze_power_task_list("Daily", {
    "action": "update",
    "index": 0,
    "Level": 8
    # LevelName 自动更新为: "毁灭的开端"
})

# 删除任务
sra_update_trailblaze_power_task_list("Daily", {
    "action": "remove",
    "index": 1
})
```

## 清体力任务列表

### 任务项结构

| 字段 | 类型 | 描述 |
|------|------|------|
| `Name` | string | 显示名称（如 "历战余响"） |
| `Id` | string | 任务标识符（如 `echo_of_war`） |
| `Level` | int | 等级编号（从 1 开始，有效范围因任务而异） |
| `LevelName` | string | 等级显示名称（**自动同步**，无需手动设置） |
| `Count` | int | 每次消耗体力 |
| `RunTimes` | int | 执行次数 |
| `AutoDetect` | bool | 自动检测等级或手动指定 |

### LevelName 自动同步

`LevelName` 根据 `Level` 自动从 SRA 前端数据计算得出。当你修改 `Level` 时，对应的 `LevelName` 会自动计算——无需手动设置。

### 有效任务 ID

| ID | 名称 | 最大等级 | 最大次数 |
|----|------|---------|---------|
| `ornament_extraction` | 饰品提取 | 13 | 6 |
| `calyx_golden` | 拟造花萼（金） | 15 | 24 |
| `calyx_crimson` | 拟造花萼（赤） | 17 | 24 |
| `stagnant_shadow` | 凝滞虚影 | 28 | 8 |
| `caver_of_corrosion` | 侵蚀隧洞 | 15 | 6 |
| `echo_of_war` | 历战余响 | 8 | 3 |

### 历战余响等级参考

| Level | LevelName |
|-------|-----------|
| 1 | 铁骸的锈冢 |
| 2 | 晨昏的回眸 |
| 3 | 心兽的战场 |
| 4 | 尘梦的赞礼 |
| 5 | 蛀星的旧靥 |
| 6 | 不死的神实 |
| 7 | 寒潮的落幕 |
| 8 | 毁灭的开端 |

## 限制

- **仅支持 Windows** - SRA 本身仅支持 Windows
- **需要 .NET 8.0** - 用于运行 SRA GUI
- **同步执行** - 任务执行会阻塞，超时时间可配置（默认 30 分钟）

## 数据来源

`TrailblazePowerTaskList` 工具使用 SRA 前端关卡数据：
- `SRAFrontend/ViewModels/TaskPageViewModel.cs`（Tasks AvaloniaList）

当 StarRailAssistant 更新关卡数据时，需要更新：
- `src/sra_mcp/tools/trailblaze_power.py` 中的 `FRONTEND_LEVELS`

## 许可证

MIT License
