# SRA MCP Server

通过模型上下文协议（MCP）控制星穹铁道助手（StarRailAssistant）的 MCP 服务器。

## 功能特性

- 读取 SRA 设置（原始 JSON 或人类可读格式）
- 使用显示名称更新 SRA 设置
- 读取任务配置（原始 JSON 或人类可读格式）
- 使用显示名称更新任务配置
- 列出可用任务配置
- 启动 SRA GUI
- 同步运行 SRA 任务
- 管理 TrailblazePowerTaskList（添加、修改、删除清体力任务）

## 安装

```bash
pip install -e .
```

## 配置

在 MCP 目录下创建 `config.json`：

```json
{
  "sra_path": "D:\\Software\\StarRailAssistant"
}
```

## MCP 客户端配置

在 Claude Code 的 MCP 设置中添加：

```json
{
  "sra-mcp": {
    "command": "python",
    "args": ["-m", "sra_mcp"],
    "cwd": "SRA_MCP"
  }
}
```

## 可用工具

### 设置工具
| 工具 | 描述 |
|------|------|
| `sra_get_settings` | 获取原始 settings.json |
| `sra_get_settings_readable` | 获取人类可读的设置 |
| `sra_update_settings` | 使用显示名称更新设置 |

### 任务配置工具
| 工具 | 描述 |
|------|------|
| `sra_list_configs` | 列出所有任务配置 |
| `sra_get_config` | 获取原始任务配置 JSON |
| `sra_get_config_readable` | 获取人类可读格式的任务配置 |
| `sra_update_config` | 使用显示名称更新任务配置 |

### 任务执行工具
| 工具 | 描述 |
|------|------|
| `sra_start` | 启动 SRA GUI |
| `sra_run_task` | 运行任务（支持超时设置） |

### 清体力任务列表工具
| 工具 | 描述 |
|------|------|
| `sra_get_trailblaze_power_task_list` | 获取清体力任务列表详情及可用任务 |
| `sra_update_trailblaze_power_task_list` | 添加、修改或删除清体力任务 |

## 使用示例

### 获取设置
```
sra_get_settings() -> {"language": 0, "appChannel": 0, ...}
```

### 获取可读设置
```
sra_get_settings_readable() -> {
  "raw": {...},
  "readable": {
    "语言": {"value": 0, "display": "简体中文", "options": ["简体中文", "English"]},
    ...
  }
}
```

### 更新设置
```
sra_update_settings({"语言": "English", "启用叠加层": "是"})
```

### 列出任务配置
```
sra_list_configs() -> ["Default", "MyConfig"]
```

### 获取任务配置
```
sra_get_config("Default") -> {"name": "Default", "enabledTasks": [true, false, ...], ...}
```

### 获取可读任务配置
```
sra_get_config_readable("Default") -> {
  "raw": {...},
  "readable": {
    "启用启动游戏": {"value": true, "display": "是", "options": ["否", "是"]},
    "启用清体力": {"value": false, "display": "否", "options": ["否", "是"]},
    "游戏通道": {"value": 0, "display": "国服", "options": ["国服", "B服"]},
    ...
  }
}
```

### 更新任务配置
```
# 启用清体力并设置补充次数
sra_update_config("Default", {
  "启用清体力": "是",
  "补充体力次数": 3,
  "启用差分宇宙": "是",
  "差分宇宙运行次数": 5,
  "货币战争模式": "标准博弈"
})
```

### 启动 SRA
```
sra_start() -> {"success": true, "message": "SRA started successfully"}
```

### 运行任务
```
sra_run_task("Default")  # 运行 Default 配置中所有已启用的任务
sra_run_task("Default", "StartGameTask")  # 运行指定任务
sra_run_task("Default", timeout=3600)  # 1 小时超时
```

### 获取清体力任务列表
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

### 添加清体力任务
```
sra_update_trailblaze_power_task_list("Daily", {
  "action": "add",
  "Name": "历战余响",
  "Id": "echo_of_war",
  "Level": 3
})
```

### 修改清体力任务
```
sra_update_trailblaze_power_task_list("Daily", {
  "action": "update",
  "index": 0,
  "Level": 8
})
```

### 删除清体力任务
```
sra_update_trailblaze_power_task_list("Daily", {
  "action": "remove",
  "index": 1
})
```

## 清体力任务列表字段说明

### 任务项结构
| 字段 | 类型 | 说明 |
|------|------|------|
| `Name` | string | 任务显示名称 |
| `Id` | string | 任务标识符（如 `calyx_crimson`、`echo_of_war`） |
| `Level` | int | 等级编号（必须在有效范围内） |
| `LevelName` | string | 等级显示名称（根据 Level 自动同步，无需手动设置） |
| `Count` | int | 每次消耗体力（最大值因任务而异） |
| `RunTimes` | int | 执行次数 |
| `AutoDetect` | bool | 自动检测等级或手动指定 |

### LevelName 自动同步

当修改 `Level` 时，`LevelName` 会根据前端数据自动更新。添加或更新任务时无需手动指定 `LevelName`。

### 可用关卡列表

使用 `sra_get_trailblaze_power_task_list` 获取每个任务的完整关卡列表：

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
        ...
        "《绒绒号》典藏版合集（欢愉）"
      ]
    }
  ]
}
```

### 有效任务 ID
| ID | 名称 | 最大等级 | 最大次数 |
|----|------|---------|---------|
| `ornament_extraction` | 饰品提取 | 13 | 6 |
| `calyx_golden` | 拟造花萼（金） | 15 | 24 |
| `calyx_crimson` | 拟造花萼（赤） | 17 | 24 |
| `stagnant_shadow` | 凝滞虚影 | 28 | 8 |
| `caver_of_corrosion` | 侵蚀隧洞 | 15 | 6 |
| `echo_of_war` | 历战余响 | 8 | 3 | |

## 任务配置字段说明

### 任务开关
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 启用启动游戏 | enabledTasks[0] | 否/是 |
| 启用清体力 | enabledTasks[1] | 否/是 |
| 启用领取奖励 | enabledTasks[2] | 否/是 |
| 启用旷宇纷争 | enabledTasks[3] | 否/是 |
| 启用任务结束 | enabledTasks[4] | 否/是 |

### 启动游戏
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 游戏通道 | startGameChannel | 国服/B服 |
| 自动登录 | startGameAutoLogin | 否/是 |
| 使用全局游戏路径 | startGameUseGlobalPath | 否/是 |

### 清体力
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 启用补充体力 | trailblazePowerReplenishEnable | 否/是 |
| 补充体力次数 | trailblazePowerReplenishTimes | - |
| 补充体力方式 | trailblazePowerReplenishWay | 指定体力/指定次数 |
| 使用助理 | trailblazePowerUseAssistant | 否/是 |
| 使用培养目标 | trailblazePowerUseBuildTarget | 否/是 |

### 领取奖励
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 领取每日实训 | receiveRewards[0] | 否/是 |
| 领取无名勋礼 | receiveRewards[1] | 否/是 |
| 领取助战奖励 | receiveRewards[2] | 否/是 |
| 领取兑换码 | receiveRewards[3] | 否/是 |
| 领取派遣奖励 | receiveRewards[4] | 否/是 |
| 领取巡星之礼 | receiveRewards[5] | 否/是 |
| 领取邮件奖励 | receiveRewards[6] | 否/是 |

### 旷宇纷争 - 差分宇宙
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 启用差分宇宙 | dUEnable | 否/是 |
| 差分宇宙运行次数 | dURunTimes | - |
| 差分宇宙使用秘技 | dUUseTechnique | 否/是 |

### 旷宇纷争 - 货币战争
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 启用货币战争 | currencyWarsEnable | 否/是 |
| 货币战争模式 | currencyWarsMode | 标准博弈/超频博弈/刷开局 |
| 货币战争难度 | currencyWarsDifficulty | 最低难度/最高难度/当前难度 |
| 货币战争运行次数 | currencyWarsRunTimes | - |
| 货币战争用户名 | currencyWarsUsername | - |

### 任务结束
| 显示名称 | JSON 字段 | 选项 |
|---------|-----------|------|
| 任务后退出应用 | afterExitApp | 否/是 |
| 任务后退出游戏 | afterExitGame | 否/是 |
| 任务后登出 | afterLogout | 否/是 |
| 任务后关机 | afterShutdown | 否/是 |
| 任务后睡眠 | afterSleep | 否/是 |

## 限制

- 仅支持 Windows（SRA 本身仅支持 Windows）
- 运行 SRA GUI 需要 .NET 8.0
- 任务执行为同步阻塞模式，默认超时 30 分钟
