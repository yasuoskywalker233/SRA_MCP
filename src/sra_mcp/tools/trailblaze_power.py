"""MCP tools for TrailblazePowerTaskList operations"""
from typing import Optional


class TrailblazePowerError(Exception):
    """Base exception for TrailblazePower operations"""
    pass


class TrailblazePowerReadError(TrailblazePowerError):
    """Raised when TrailblazePower config cannot be read"""
    pass


class InvalidOperationError(TrailblazePowerError):
    """Raised when operation type is invalid"""
    pass


class IndexOutOfRangeError(TrailblazePowerError):
    """Raised when task list index is out of range"""
    pass


class InvalidTaskIdError(TrailblazePowerError):
    """Raised when task ID is not valid"""
    pass


class InvalidLevelError(TrailblazePowerError):
    """Raised when level is out of valid range for a task"""
    pass


class CountExceedsMaxError(TrailblazePowerError):
    """Raised when Count exceeds max_count for a task"""
    pass


class TypeValidationError(TrailblazePowerError):
    """Raised when field type validation fails"""
    pass


import tomllib
from pathlib import Path


def _get_sra_path(sra_config) -> Path:
    """Get SRA path from config"""
    from sra_mcp.config import SRAConfig
    if sra_config is None:
        sra_config = SRAConfig.load()
    return Path(sra_config.sra_path)


# =============================================================================
# Frontend Levels Data
# =============================================================================
# Data Source: SRAFrontend/ViewModels/TaskPageViewModel.cs
#   -> Tasks AvaloniaList<TrailblazePowerTask>
#   -> Each TrailblazePowerTask has a Levels: string[] array
#
# IMPORTANT: When StarRailAssistant is updated, check if Levels arrays changed!
#   1. Open SRAFrontend/ViewModels/TaskPageViewModel.cs
#   2. Find the Tasks AvaloniaList (around line 71)
#   3. Copy the Levels arrays from each new(AddTaskItem) {...} block
#   4. Replace the corresponding entries in this dictionary
#
# Index 0 is always the placeholder "---选择副本---"
# Level N corresponds to levels[N] (e.g., Level 1 = levels[1])
#
# Data Structure per task:
#   "task_id": [
#       "---选择副本---",  <- Index 0, not a valid level
#       "Level 1 Name",
#       "Level 2 Name",
#       ...
#   ]
#
# Max valid Level = len(levels) - 1 (because index 0 is placeholder)
# =============================================================================
FRONTEND_LEVELS: dict[str, list[str]] = {
    "ornament_extraction": [
        "---选择副本---",
        "鎏金追忆（朋克洛德/千星城）",
        "西风丛中（翁法罗斯/天国@直播间）",
        "月下朱殷（妖精/海隅）",
        "纷争不休（拾骨地/巨树）",
        "蠹役饥肠（露莎卡/蕉乐园）",
        "永恒笑剧（都蓝/劫火）",
        "伴你入眠（茨冈尼亚/出云显世）",
        "天剑如雨（格拉默/匹诺康尼）",
        "孽果盘生（繁星/龙骨）",
        "百年冻土（贝洛伯格/萨尔索图）",
        "温柔话语（公司/差分机）",
        "浴火钢心（塔利亚/翁瓦克）",
        "坚城不倒（太空封印站/仙舟）",
    ],
    "calyx_golden": [
        "---选择副本---",
        "回忆之蕾（二相乐园）",
        "以太之蕾（二相乐园）",
        "珍藏之蕾（二相乐园）",
        "回忆之蕾（翁法罗斯）",
        "以太之蕾（翁法罗斯）",
        "珍藏之蕾（翁法罗斯）",
        "回忆之蕾（匹诺康尼）",
        "以太之蕾（匹诺康尼）",
        "珍藏之蕾（匹诺康尼）",
        "回忆之蕾（仙舟罗浮）",
        "以太之蕾（仙舟罗浮）",
        "珍藏之蕾（仙舟罗浮）",
        "回忆之蕾（雅利洛VI）",
        "以太之蕾（雅利洛VI）",
        "珍藏之蕾（雅利洛VI）",
    ],
    "calyx_crimson": [
        "---选择副本---",
        "月狂獠牙（毁灭）",
        "净世残刃（毀灭）",
        "神体琥珀（存护）",
        "琥珀的坚守（存护）",
        "天谴血矛（巡猎）",
        "逆时一击（巡猎）",
        "逐星之矢（巡猎）",
        "万象果实（丰饶）",
        "永恒之花（丰饶）",
        "精致色稿（智识）",
        "智识之钥（智识）",
        "天外乐章（同谐）",
        "群星乐章（同谐）",
        "法吉娜之心（虚无）",
        "焚天之魔（虚无）",
        "沉沦黑曜（虚无）",
        "阿赖耶华（记忆）",
        "《绒绒号》典藏版合集（欢愉）",
    ],
    "stagnant_shadow": [
        "---选择副本---",
        "侵略凝块（物理）",
        "星际和平工作证（物理）",
        "幽府通令（物理）",
        "铁狼碎齿（物理）",
        "明辉日珥（火）",
        "忿火之心（火）",
        "过热钢刀（火）",
        "恒温晶壳（火）",
        "海妖残鰭（冰）",
        "冷藏梦箱（冰）",
        "苦寒晶壳（冰）",
        "风雪之角（冰）",
        "狂雷扫弦（雷）",
        "兽馆之钉（雷）",
        "炼形者雷枝（雷）",
        "往日之影的雷冠（雷）",
        "暮辉烬蕾（风）",
        "一杯酪酊的时代（风）",
        "无人遗垢（风）",
        "暴风之眼（风）",
        "暗帷月华（量子）",
        "炙梦喷枪（量子）",
        "苍猿之钉（量子）",
        "虚幻铸铁（量子）",
        "纷争前兆（虚数）",
        "一曲和弦的幻景（虚数）",
        "镇灵敕符（虚数）",
        "往日之影的金饰（虚数）",
    ],
    "caver_of_corrosion": [
        "---选择副本---",
        "魔占之径（魔法少女/卜者）",
        "隐救之径（救世主/隐士）",
        "雳勇之径（女武神/船长）",
        "弦歌之径（英豪/诗人）",
        "迷识之径（司铎套/学者套）",
        "勇骑之径（铁骑套/勇烈套）",
        "梦潜之径（死水/钟表匠）",
        "幽冥之径（大公/幽囚）",
        "药使之径（莳者/信使）",
        "野焰之径（火匠/废土客）",
        "圣颂之径（圣骑/乐队）",
        "睿智之径（铁卫/量子套）",
        "漂泊之径（过客/快枪手）",
        "迅拳之径（拳皇/怪盗）",
        "霜风之径（冰/风套）",
    ],
    "echo_of_war": [
        "---选择副本---",
        "铁骸的锈冢",
        "晨昏的回眸",
        "心兽的战场",
        "尘梦的赞礼",
        "蛀星的旧靥",
        "不死的神实",
        "寒潮的落幕",
        "毁灭的开端",
    ],
}

# Frontend Trailblaze_power Tasks Data
# Data Source: SRAFrontend/ViewModels/TaskPageViewModel.cs
#   -> Tasks AvaloniaList<TrailblazePowerTask>
#   -> Each TrailblazePowerTask has Title and Id
# key:Title
# value:Id
FRONTEND_TASKSNAME_TASKID : dict[str,str] = {
    "饰品提取" : "ornament_extraction",
    "拟造花萼（金）" : "calyx_golden",
    "拟造花萼（赤）" : "calyx_crimson",
    "凝滞虚影" : "stagnant_shadow",
    "侵蚀隧洞" : "caver_of_corrosion",
    "历战余响" : "echo_of_war"
}

# 通过task_id(模式名)和level下标获取副本名字
def _get_level_name_from_frontend(task_id: str, level: int) -> str:
    """
    Get LevelName from Level and task_id using FRONTEND_LEVELS data.

    This function maps Level (1-based) to LevelName using the frontend's
    hardcoded Levels array from TaskPageViewModel.cs.

    Args:
        task_id: Task identifier (e.g., "calyx_crimson", "echo_of_war")
        level: Level number (1-based, where 1 is the first valid level)

    Returns:
        LevelName string from FRONTEND_LEVELS, or empty string if not found

    Note:
        Level 0 is not valid (it's the "---选择副本---" placeholder).
        Level 1 corresponds to FRONTEND_LEVELS[task_id][1].
    """
    if task_id not in FRONTEND_LEVELS:
        return ""
    levels = FRONTEND_LEVELS[task_id]
    # Level is 1-based, levels[0] is placeholder "---选择副本---"
    if 0 <= level < len(levels):
        return levels[level]
    return ""

# 修改task_item的Id(模式)和level(副本下标)后，更新LevelName(关卡名)，避免破坏Json文件的数据正确性
def _sync_level_name(task_item: dict) -> None:
    """
    Sync LevelName in a task item based on Level and Id.

    This function is called after updating Level to automatically
    update LevelName to match the new level's display name.

    Args:
        task_item: Task item dict to modify in-place
                   Must contain "Id" and "Level" keys

    Example:
        task_item = {"Id": "echo_of_war", "Level": 3}
        _sync_level_name(task_item)
        # task_item now has "LevelName": "心兽的战场"
    """
    task_id = task_item.get("Id")
    level = task_item.get("Level")
    if task_id and level:
        task_item["LevelName"] = _get_level_name_from_frontend(task_id, level)

# 从SRA/tasks/config/trailblaze_power.toml中读取所有可选任务
def load_trailblaze_power_config(sra_config=None) -> dict[str, dict]:
    """
    Load and parse trailblaze_power.toml.

    Returns dict mapping task_id to task_info:
    {
        "calyx_crimson": {
            "name": "拟造花萼（赤）",
            "max_count": 24,
        },
        ...
    }
    """
    sra_path = _get_sra_path(sra_config)
    toml_path = sra_path / "tasks" / "config" / "trailblaze_power.toml"

    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
    except FileNotFoundError:
        raise TrailblazePowerReadError(f"trailblaze_power.toml not found at {toml_path}")

    result = {}
    subtasks = data.get("subtasks", {})
    for task_id, task_info in subtasks.items():
        max_count = task_info.get("max_count", 0)
        # levels = task_info.get("levels", [])

        result[task_id] = {
            "name": task_info.get("name", task_id),
            "max_count": max_count,
            # "max_level": max_level,
            # "levels": levels,
        }
    return result

# 根据任务id获取任务名
def get_task_name_by_task_id(task_id,sra_config=None) -> str:
    sra_path = _get_sra_path(sra_config)
    toml_path = sra_path / "tasks" / "config" / "trailblaze_power.toml"
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
    except FileNotFoundError:
        raise TrailblazePowerReadError(f"trailblaze_power.toml not found at {toml_path}")
    subtasks = data.get("subtasks", {})
    return subtasks.get(task_id).get("name") 

VALID_OPERATIONS = {"add", "update", "remove"}
VALID_FIELDS = {"Id", "Level", "Count", "RunTimes", "AutoDetect", "Name", "LevelName"}

# 验证数据正确性
def validate_task_fields(
    task_data: dict,
    task_config: dict[str, dict],
    allow_partial: bool = False,
    is_update: bool = False
) -> list[str]:
    """
    Validate task fields.

    Args:
        task_data: Task field values to validate
        task_config: Loaded trailblaze_power.toml config
        allow_partial: If True, not all fields are required (for update)
        is_update: If True, this is an update operation

    Returns:
        List of error messages (empty if valid)

    Raises:
        TypeValidationError: When field type is wrong
        InvalidTaskIdError: When Id is not valid
        InvalidLevelError: When Level is out of range
        CountExceedsMaxError: When Count exceeds max_count
    """
    errors = []

    # Check for unknown fields
    unknown_fields = set(task_data.keys()) - VALID_FIELDS
    if unknown_fields:
        errors.append(f"未知字段: {unknown_fields}")

    # Validate Id if present
    task_id = task_data.get("Id")
    if task_id is not None:
        if not isinstance(task_id, str):
            errors.append(f"字段 Id 必须为字符串，当前为 {type(task_id).__name__}")
        elif task_id not in task_config:
            valid_ids = list(task_config.keys())
            errors.append(f"无效任务 ID：{task_id}，有效值为 {valid_ids}")

    # Validate Level if present
    level = task_data.get("Level")
    if level is not None:
        if not isinstance(level, int):
            errors.append(f"字段 Level 必须为整数，当前为 {type(level).__name__}")
        elif level <= 0:
            errors.append(f"字段 Level 必须为正整数，当前为 {level}")
        elif task_id is not None:
            # Use frontend levels for max_level validation (more accurate)
            frontend_levels = FRONTEND_LEVELS.get(task_id)
            if frontend_levels:
                max_level = len(frontend_levels) - 1  # -1 because index 0 is placeholder
                if level > max_level:
                    task_name = task_config.get(task_id, {}).get("name", task_id)
                    errors.append(f"任务 {task_name} 的 Level 必须为 1-{max_level}，当前为 {level}")

    # Validate Count if present
    count = task_data.get("Count")
    if count is not None:
        if not isinstance(count, int):
            errors.append(f"字段 Count 必须为整数，当前为 {type(count).__name__}")
        elif count <= 0:
            errors.append(f"字段 Count 必须为正整数，当前为 {count}")
        elif task_id is not None and task_id in task_config:
            max_count = task_config[task_id]["max_count"]
            if count > max_count:
                task_name = task_config[task_id]["name"]
                errors.append(f"任务 {task_name} 的 Count 不能超过 {max_count}，当前为 {count}")

    # Validate RunTimes if present
    run_times = task_data.get("RunTimes")
    if run_times is not None:
        if not isinstance(run_times, int):
            errors.append(f"字段 RunTimes 必须为整数，当前为 {type(run_times).__name__}")
        elif run_times <= 0:
            errors.append(f"字段 RunTimes 必须为正整数，当前为 {run_times}")

    # Validate AutoDetect if present
    auto_detect = task_data.get("AutoDetect")
    if auto_detect is not None:
        if not isinstance(auto_detect, bool):
            errors.append(f"字段 AutoDetect 必须为布尔值，当前为 {type(auto_detect).__name__}")

    # Validate Name if present (must be string)
    name = task_data.get("Name")
    if name is not None and not isinstance(name, str):
        errors.append(f"字段 Name 必须为字符串，当前为 {type(name).__name__}")

    # Validate LevelName if present (must be string)
    level_name = task_data.get("LevelName")
    if level_name is not None and not isinstance(level_name, str):
        errors.append(f"字段 LevelName 必须为字符串，当前为 {type(level_name).__name__}")

    return errors

# 获取目标配置的清体力任务列表 和 所有可用任务列表
# 目标配置 和 所有可用 都走这个
def get_trailblaze_power_task_list(config_name: str,sra_config=None) -> dict:
    """
    Get TrailblazePowerTaskList details for a config.

    Args:
        config_name: Name of the task config (e.g., "Daily")
        sra_config: Optional SRAConfig instance

    Returns:
        {
            "config_name": "Daily",
            "task_list": [...],  # Current task list
            "available_tasks": [
                {"id": "calyx_crimson", "name": "拟造花萼（赤）", "max_count": 24, "all_levels": {"levelName": "月狂獠牙（毁灭）", "index": 1}},
                ...
            ]
        }
    """
    from sra_mcp.tools.task_config import get_task_config, TaskConfigNotFoundError, TaskConfigReadError
    # 加载sra中的所有可用任务
    task_config = load_trailblaze_power_config(sra_config)
    
    # 加载目标配置的任务
    try:
        config_data = get_task_config(config_name, sra_config)
    except (TaskConfigNotFoundError, TaskConfigReadError) as e:
        raise TrailblazePowerReadError(f"Failed to read config '{config_name}': {e}")
    task_list = config_data.get("TrailblazePowerTaskList", [])

    # 构建可用任务列表
    available_tasks = []
    for task_id, info in task_config.items():
        levels = FRONTEND_LEVELS.get(task_id, []) #当前任务Id的所有可用副本
        available_tasks.append({
            "id": task_id,
            "name": info["name"],
            # "max_level": len(FRONTEND_LEVELS.get(task_id,[]))-1,
            "max_count": info["max_count"],
            "all_levels": [
                {"levelName":level, "index":i}
                for i,level in enumerate(levels[1:],start=1) #0是选择副本，从1开始
            ],
        })

    # 返回结果
    return {
        "config_name": config_name,
        "task_list": task_list,
        "available_tasks": available_tasks,
    }

# 更新目标配置的清体力列表任务项(添加/删除/更新)
def update_trailblaze_power_task_list(
    config_name: str,
    operation: dict,
    sra_config=None
) -> dict:
    """
    Update TrailblazePowerTaskList with an atomic operation.

    Args:
        config_name: Name of the task config (e.g., "Daily")
        operation: Operation dict with keys:
            - action: "add" | "update" | "remove"
            - index: int (for update/remove)
            - Name, Id, Level, LevelName, Count, RunTimes, AutoDetect (for add/update)
        sra_config: Optional SRAConfig instance

    Returns:
        {
            "success": True,
            "message": "已添加关卡：xxx",
            "data": {"trailblaze_power_task_list": [...]}
        }
    """
    from sra_mcp.tools.task_config import get_task_config, TaskConfigNotFoundError, TaskConfigReadError
    import json

    # 加载可选关卡
    task_config = load_trailblaze_power_config(sra_config)

    # 验证操作合法性
    action = operation.get("action")
    if action not in VALID_OPERATIONS:
        raise InvalidOperationError(f"无效操作：{action}，有效值为 add/update/remove")

    # 加载当前的清体力任务配置
    try:
        config_data = get_task_config(config_name, sra_config)
    except (TaskConfigNotFoundError, TaskConfigReadError) as e:
        raise TrailblazePowerReadError(f"Failed to read config '{config_name}': {e}")
    task_list = config_data.get("TrailblazePowerTaskList", [])

    # 执行操作
    if action == "add": # 添加
        # 验证必要字段
        required_fields = {"Id", "Level"}
        missing_fields = required_fields - set(operation.keys())
        if missing_fields:
            raise InvalidOperationError(f"添加操作缺少必需字段: {missing_fields}")

        # 验证字段合法性
        errors = validate_task_fields(operation, task_config, allow_partial=False, is_update=False)
        if errors:
            raise TypeValidationError("; ".join(errors))

        # Build new task item
        new_task = {
            "Name": get_task_name_by_task_id(operation["Id"],sra_config=sra_config),
            "Id": operation["Id"],
            "Level": operation["Level"],
            "LevelName": _get_level_name_from_frontend(operation["Id"], operation["Level"]),
            "Count": operation.get("Count", 1),
            "RunTimes": operation.get("RunTimes", 1),
            "AutoDetect": operation.get("AutoDetect", True),
        }
        task_list.append(new_task)
        task_name = new_task["Name"]
        message = f"已添加关卡：{task_name}"

    elif action == "update": # 更新
        # 索引合法性
        index = operation.get("index")
        if index is None:
            raise InvalidOperationError("更新操作需要指定 index")
        if not isinstance(index, int) or index < 0 or index >= len(task_list):
            raise IndexOutOfRangeError(f"索引 {index} 超出范围，当前列表长度为 {len(task_list)}")
        # 检查是否有更新
        update_fields = {k: v for k, v in operation.items() if k in VALID_FIELDS and k != "index"}
        if not update_fields:
            raise InvalidOperationError("更新操作至少需要提供一个要更新的字段")
        # 补全operation
        if not "LevelName" in operation:
            operation["LevelName"] = _get_level_name_from_frontend(operation["Id"], operation["Level"])
            update_fields["LevelName"] = operation["LevelName"]
        if not "Name" in operation:
            operation["Name"] = get_task_name_by_task_id(operation["Id"],sra_config=sra_config)
            update_fields["Name"] = operation["Name"]

        # 检查operation合法性
        errors = validate_task_fields(update_fields, task_config, allow_partial=True, is_update=True)
        if errors:
            raise TypeValidationError("; ".join(errors))

        # 应用更新
        current_task = task_list[index]
        current_task.update(update_fields)
        # # Sync LevelName if Level was changed
        # if "Level" in update_fields:
        #     _sync_level_name(current_task)
        task_name = current_task["Name"]
        message = f"已更新关卡：{task_name}"

    elif action == "remove": # 移除
        index = operation.get("index")
        if index is None:
            raise InvalidOperationError("删除操作需要指定 index")
        if not isinstance(index, int) or index < 0 or index >= len(task_list):
            raise IndexOutOfRangeError(f"索引 {index} 超出范围，当前列表长度为 {len(task_list)}")
        removed_task = task_list.pop(index)
        task_name = removed_task.get("Name", removed_task.get("Id", ""))
        message = f"已删除关卡：{task_name}"

    # Save updated config
    config_data["TrailblazePowerTaskList"] = task_list

    # Write back to file
    from sra_mcp.config import SRAConfig
    if sra_config is None:
        sra_config = SRAConfig.load()

    configs_dir = sra_config.get_configs_dir()
    config_path = configs_dir / f"{config_name}.json"

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=True)
    except Exception as e:
        raise TrailblazePowerError(f"Failed to write config: {e}")

    return {
        "success": True,
        "message": message,
        "data": {
            "trailblaze_power_task_list": task_list
        }
    }
