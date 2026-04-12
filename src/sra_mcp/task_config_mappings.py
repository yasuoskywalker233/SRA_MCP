"""Task configuration field mappings for SRA task configs."""
from typing import Any

# Task config field mappings
# Based on Config.cs and task implementations
# NOTE: All json_field values use PascalCase to match actual SRA config files
TASK_CONFIG_FIELDS: dict[str, dict[str, Any]] = {
    # === 基本配置 ===
    "配置名称": {"json_field": "Name", "type": "str"},
    "配置版本": {"json_field": "Version", "type": "int"},

    # === 任务开关 ===
    "启用启动游戏": {"json_field": "EnabledTasks", "options": ["否", "是"], "type": "bool", "index": 0},
    "启用清体力": {"json_field": "EnabledTasks", "options": ["否", "是"], "type": "bool", "index": 1},
    "启用领取奖励": {"json_field": "EnabledTasks", "options": ["否", "是"], "type": "bool", "index": 2},
    "启用旷宇纷争": {"json_field": "EnabledTasks", "options": ["否", "是"], "type": "bool", "index": 3},
    "启用任务结束": {"json_field": "EnabledTasks", "options": ["否", "是"], "type": "bool", "index": 4},

    # === 启动游戏 (StartGameTask) ===
    "游戏通道": {"json_field": "StartGameChannel", "options": ["国服", "B服"], "type": "int"},
    "游戏路径": {"json_field": "StartGamePath", "type": "str"},
    "使用全局游戏路径": {"json_field": "StartGameUseGlobalPath", "options": ["否", "是"], "type": "bool"},
    "自动登录": {"json_field": "StartGameAutoLogin", "options": ["否", "是"], "type": "bool"},
    "总是登录": {"json_field": "StartGameAlwaysLogin", "options": ["否", "是"], "type": "bool"},
    "启动用户名": {"json_field": "StartGameUsername", "type": "str"},
    # StartGamePassword 是加密的，不暴露

    # === 清体力 (TrailblazePowerTask) ===
    "启用补充体力": {"json_field": "TrailblazePowerReplenishEnable", "options": ["否", "是"], "type": "bool"},
    "补充体力次数": {"json_field": "TrailblazePowerReplenishTimes", "type": "int"},
    "补充体力方式": {"json_field": "TrailblazePowerReplenishWay", "options": ["指定体力", "指定次数"], "type": "int"},
    "使用助理": {"json_field": "TrailblazePowerUseAssistant", "options": ["否", "是"], "type": "bool"},
    "使用培养目标": {"json_field": "TrailblazePowerUseBuildTarget", "options": ["否", "是"], "type": "bool"},
    # TrailblazePowerTaskList 是数组，复杂对象，需要特殊处理

    # === 领取奖励 (ReceiveRewardsTask) ===
    # ReceiveRewards 是一个 bool 数组
    "领取每日实训": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 0},
    "领取无名勋礼": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 1},
    "领取助战奖励": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 2},
    "领取兑换码": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 3},
    "领取派遣奖励": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 4},
    "领取巡星之礼": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 5},
    "领取邮件奖励": {"json_field": "ReceiveRewards", "options": ["否", "是"], "type": "bool", "index": 6},
    "兑换码列表": {"json_field": "ReceiveRewardRedeemCodes", "type": "str"},

    # === 旷宇纷争 (CosmicStrifeTask) ===
    # 差分宇宙 (DifferentialUniverse)
    "启用差分宇宙": {"json_field": "DUEnable", "options": ["否", "是"], "type": "bool"},
    "差分宇宙模式": {"json_field": "DUMode", "type": "int"},
    "差分宇宙策略": {"json_field": "DUPolicy", "type": "int"},
    "差分宇宙运行次数": {"json_field": "DURunTimes", "type": "int"},
    "差分宇宙使用秘技": {"json_field": "DUUseTechnique", "options": ["否", "是"], "type": "bool"},

    # 货币战争 (CurrencyWars)
    "启用货币战争": {"json_field": "CurrencyWarsEnable", "options": ["否", "是"], "type": "bool"},
    "货币战争模式": {"json_field": "CurrencyWarsMode", "options": ["标准博弈", "超频博弈", "刷开局"], "type": "int"},
    "货币战争难度": {"json_field": "CurrencyWarsDifficulty", "options": ["最低难度", "最高难度", "当前难度"], "type": "int"},
    "货币战争运行次数": {"json_field": "CurrencyWarsRunTimes", "type": "int"},
    "货币战争策略": {"json_field": "CurrencyWarsStrategy", "type": "str"},
    "货币战争策略索引": {"json_field": "CurrencyWarsStrategyIndex", "type": "int"},
    "货币战争用户名": {"json_field": "CurrencyWarsUsername", "type": "str"},

    # 刷开局 (CwRs - Currency Wars Reroll Start)
    "刷开局期望投资环境": {"json_field": "CwRsInvestEnvironments", "type": "str"},
    "刷开局期望投资策略": {"json_field": "CwRsInvestStrategies", "type": "str"},
    "刷开局期望Boss名称": {"json_field": "CwRsBossNames", "type": "str"},
    "刷开局期望Boss词条": {"json_field": "CwRsBossAffixes", "type": "str"},
    "刷开局投资策略阶段": {"json_field": "CwRsInvestStrategyStage", "type": "int"},
    "刷开局最大重试": {"json_field": "CwRsMaxRetry", "type": "int"},

    # === 任务结束 (MissionAccomplishTask) ===
    "任务后退出应用": {"json_field": "AfterExitApp", "options": ["否", "是"], "type": "bool"},
    "任务后退出游戏": {"json_field": "AfterExitGame", "options": ["否", "是"], "type": "bool"},
    "任务后登出": {"json_field": "AfterLogout", "options": ["否", "是"], "type": "bool"},
    "任务后关机": {"json_field": "AfterShutdown", "options": ["否", "是"], "type": "bool"},
    "任务后睡眠": {"json_field": "AfterSleep", "options": ["否", "是"], "type": "bool"},
}


class TaskConfigJsonToDisplayMapper:
    """Map JSON task config to human-readable format"""

    def map(self, raw_config: dict) -> dict:
        """Convert raw JSON config to readable format"""
        result = {}

        for display_name, field_info in TASK_CONFIG_FIELDS.items():
            json_field = field_info["json_field"]
            field_type = field_info["type"]
            options = field_info.get("options", [])

            # Handle array fields like enabledTasks and receiveRewards
            if "index" in field_info:
                arr = raw_config.get(json_field, [])
                if isinstance(arr, list) and field_info["index"] < len(arr):
                    raw_value = arr[field_info["index"]]
                else:
                    raw_value = False if field_type == "bool" else 0
            else:
                if json_field not in raw_config:
                    continue
                raw_value = raw_config[json_field]

            # Map value to display string
            if field_type == "bool":
                display = "是" if raw_value else "否"
            elif field_type == "int" and options:
                idx = raw_value if isinstance(raw_value, int) else 0
                display = options[idx] if 0 <= idx < len(options) else str(raw_value)
            else:
                display = str(raw_value)

            result[display_name] = {
                "value": raw_value,
                "display": display,
                "options": options if options else [],
            }

        # Handle special fields that are arrays
        if "TrailblazePowerTaskList" in raw_config:
            result["清体力任务列表"] = {
                "value": raw_config["TrailblazePowerTaskList"],
                "display": f"{len(raw_config['TrailblazePowerTaskList'])} 个关卡",
                "options": [],
            }

        return result


class TaskConfigDisplayToJsonMapper:
    """Map human-readable display names back to JSON values"""

    def map(self, display_config: dict) -> dict:
        """Convert display config back to JSON format"""
        result = {}

        # First, handle array fields
        enabled_tasks_idx = {}
        receive_rewards_idx = {}

        for display_name, display_value in display_config.items():
            if display_name not in TASK_CONFIG_FIELDS:
                continue

            field_info = TASK_CONFIG_FIELDS[display_name]
            json_field = field_info["json_field"]
            field_type = field_info["type"]
            options = field_info.get("options", [])

            # Handle array fields
            if "index" in field_info:
                idx = field_info["index"]
                if field_type == "bool":
                    bool_val = display_value == "是"
                    if json_field == "EnabledTasks":
                        enabled_tasks_idx[idx] = bool_val
                    elif json_field == "ReceiveRewards":
                        receive_rewards_idx[idx] = bool_val
                continue

            # Handle normal fields
            if field_type == "bool":
                result[json_field] = display_value == "是"
            elif field_type == "int" and options:
                try:
                    opt_idx = options.index(display_value)
                    result[json_field] = opt_idx
                except ValueError:
                    result[json_field] = display_value
            elif field_type == "int":
                result[json_field] = int(display_value)
            elif field_type == "float":
                result[json_field] = float(display_value)
            else:
                result[json_field] = display_value

        # Convert array indices to full arrays
        if enabled_tasks_idx:
            # Start with defaults, then apply updates
            result["EnabledTasks"] = [False] * 5
            for idx, val in enabled_tasks_idx.items():
                result["EnabledTasks"][idx] = val

        if receive_rewards_idx:
            # Start with defaults, then apply updates
            if "ReceiveRewards" not in result:
                result["ReceiveRewards"] = [True] * 7
            for idx, val in receive_rewards_idx.items():
                result["ReceiveRewards"][idx] = val

        return result
