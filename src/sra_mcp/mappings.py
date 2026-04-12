"""Settings field mappings between JSON values and human-readable display names."""
from typing import Any

SETTINGS_FIELDS: dict[str, dict[str, Any]] = {
    # int fields with options - Language/Channel settings
    "语言": {"json_field": "language", "options": ["简体中文", "English"], "type": "int"},
    "更新通道": {"json_field": "appChannel", "options": ["稳定版", "测试版"], "type": "int"},
    "下载通道": {"json_field": "downloadChannel", "options": ["Mirror", "GitHub"], "type": "int"},
    "游戏通道": {"json_field": "startGameChannel", "options": ["国服", "B服"], "type": "int"},

    # bool fields - General notifications and features
    "允许通知": {"json_field": "allowNotifications", "options": ["否", "是"], "type": "bool"},
    "允许邮件通知": {"json_field": "allowEmailNotifications", "options": ["否", "是"], "type": "bool"},
    "允许系统通知": {"json_field": "allowSystemNotifications", "options": ["否", "是"], "type": "bool"},
    "启用自动更新": {"json_field": "enableAutoUpdate", "options": ["否", "是"], "type": "bool"},
    "启用最小化到托盘": {"json_field": "enableMinimizeToTray", "options": ["否", "是"], "type": "bool"},
    "启用开机自启动": {"json_field": "enableStartupLaunch", "options": ["否", "是"], "type": "bool"},
    "启用叠加层": {"json_field": "isOverlayEnabled", "options": ["否", "是"], "type": "bool"},
    "启用叠加层调试信息": {"json_field": "isOverlayDebugInfoEnabled", "options": ["否", "是"], "type": "bool"},
    "自动检测游戏路径": {"json_field": "isAutoDetectGamePath", "options": ["否", "是"], "type": "bool"},
    "启用启动参数": {"json_field": "launchArgumentsEnabled", "options": ["否", "是"], "type": "bool"},
    "无边框窗口": {"json_field": "launchArgumentsPopupWindow", "options": ["否", "是"], "type": "bool"},
    "使用CMD启动游戏": {"json_field": "launchWithCmd", "options": ["否", "是"], "type": "bool"},
    "开发者模式": {"json_field": "isDeveloperMode", "options": ["否", "是"], "type": "bool"},
    "保存OCR截图": {"json_field": "isSaveOcrImage", "options": ["否", "是"], "type": "bool"},
    "使用Python后端": {"json_field": "isUsingPython", "options": ["否", "是"], "type": "bool"},

    # bool fields - Notification channels
    "启用Webhook通知": {"json_field": "allowWebhookNotifications", "options": ["否", "是"], "type": "bool"},
    "启用Telegram通知": {"json_field": "allowTelegramNotifications", "options": ["否", "是"], "type": "bool"},
    "Telegram启用代理": {"json_field": "telegramProxyEnabled", "options": ["否", "是"], "type": "bool"},
    "Telegram发送图片": {"json_field": "telegramSendImage", "options": ["否", "是"], "type": "bool"},
    "启用ServerChan通知": {"json_field": "allowServerChanNotifications", "options": ["否", "是"], "type": "bool"},
    "启用OneBot通知": {"json_field": "allowOneBotNotifications", "options": ["否", "是"], "type": "bool"},
    "OneBot发送图片": {"json_field": "oneBotSendImage", "options": ["否", "是"], "type": "bool"},
    "启用Bark通知": {"json_field": "allowBarkNotifications", "options": ["否", "是"], "type": "bool"},
    "启用飞书通知": {"json_field": "allowFeishuNotifications", "options": ["否", "是"], "type": "bool"},
    "启用企业微信通知": {"json_field": "allowWeComNotifications", "options": ["否", "是"], "type": "bool"},
    "企业微信发送图片": {"json_field": "weComSendImage", "options": ["否", "是"], "type": "bool"},
    "启用钉钉通知": {"json_field": "allowDingTalkNotifications", "options": ["否", "是"], "type": "bool"},
    "启用Discord通知": {"json_field": "allowDiscordNotifications", "options": ["否", "是"], "type": "bool"},
    "Discord发送图片": {"json_field": "discordSendImage", "options": ["否", "是"], "type": "bool"},
    "启用xxtui通知": {"json_field": "allowXxtuiNotifications", "options": ["否", "是"], "type": "bool"},

    # str fields with options
    "显示模式": {"json_field": "launchArgumentsFullScreenMode", "options": ["窗口化", "全屏"], "type": "str"},

    # str fields without options
    "邮件接收地址": {"json_field": "emailReceiver", "type": "str"},
    "邮件发送地址": {"json_field": "emailSender", "type": "str"},
    "SMTP服务器": {"json_field": "smtpServer", "type": "str"},
    "背景图路径": {"json_field": "backgroundImagePath", "type": "str"},
    "后端启动参数": {"json_field": "backendArguments", "type": "str"},
    "Python解释器路径": {"json_field": "pythonPath", "type": "str"},
    "Python主程序路径": {"json_field": "pythonMainPy", "type": "str"},
    "启动参数窗口尺寸": {"json_field": "launchArgumentsScreenSize", "type": "str"},
    "高级启动参数": {"json_field": "launchArgumentsAdvanced", "type": "str"},
    "Webhook URL": {"json_field": "webhookUrl", "type": "str"},
    "Telegram Bot Token": {"json_field": "telegramBotToken", "type": "str"},
    "Telegram 聊天ID": {"json_field": "telegramChatId", "type": "str"},
    "Telegram 代理地址": {"json_field": "telegramProxyAddress", "type": "str"},
    "ServerChan Key": {"json_field": "serverChanKey", "type": "str"},
    "OneBot URL": {"json_field": "oneBotUrl", "type": "str"},
    "OneBot Token": {"json_field": "oneBotToken", "type": "str"},
    "OneBot 群组ID": {"json_field": "oneBotGroupId", "type": "str"},
    "Bark 密钥": {"json_field": "barkKey", "type": "str"},
    "飞书 Webhook": {"json_field": "feishuWebhook", "type": "str"},
    "企业微信 Webhook": {"json_field": "weComWebhook", "type": "str"},
    "钉钉 Webhook": {"json_field": "dingTalkWebhook", "type": "str"},
    "Discord Webhook": {"json_field": "discordWebhook", "type": "str"},
    "xxtui URL": {"json_field": "xxtuiUrl", "type": "str"},
    "xxtui Token": {"json_field": "xxtuiToken", "type": "str"},
    "游戏路径": {"json_field": "gamePath", "type": "str"},
    "启动路径": {"json_field": "startGamePath", "type": "str"},

    # int fields without options
    "SMTP端口": {"json_field": "smtpPort", "type": "int"},
    "游戏路径索引": {"json_field": "gamePathIndex", "type": "int"},
    "默认页面": {"json_field": "defaultPage", "type": "int"},

    # float fields
    "识图置信度阈值": {"json_field": "confidenceThreshold", "type": "float"},
    "背景图不透明度": {"json_field": "backgroundOpacity", "type": "float"},
    "控制面板不透明度": {"json_field": "ctrlPanelOpacity", "type": "float"},

    # hotkey fields (str)
    "活动快捷键": {"json_field": "ActivityHotkey", "type": "str"},
    "纪行快捷键": {"json_field": "ChronicleHotkey", "type": "str"},
    "卡池快捷键": {"json_field": "WarpHotkey", "type": "str"},
    "指南快捷键": {"json_field": "GuideHotkey", "type": "str"},
    "地图快捷键": {"json_field": "MapHotkey", "type": "str"},
    "秘技快捷键": {"json_field": "TechniqueHotkey", "type": "str"},
    "启动/停止快捷键": {"json_field": "StartStopHotkey", "type": "str"},
}


class JsonToDisplayMapper:
    def map(self, raw_settings: dict) -> dict:
        """Convert raw JSON settings to readable format"""
        result = {}
        for display_name, field_info in SETTINGS_FIELDS.items():
            json_field = field_info["json_field"]
            if json_field not in raw_settings:
                continue

            raw_value = raw_settings[json_field]
            options = field_info.get("options", [])
            field_type = field_info["type"]

            # Map value to display string
            if field_type == "bool":
                display = "是" if raw_value else "否"
            elif field_type == "int" and options:
                idx = raw_value if isinstance(raw_value, int) else 0
                display = options[idx] if 0 <= idx < len(options) else str(raw_value)
            elif field_type == "str" and options:
                idx = raw_value if isinstance(raw_value, int) else 0
                display = options[idx] if 0 <= idx < len(options) else raw_value
            else:
                display = str(raw_value)

            result[display_name] = {
                "value": raw_value,
                "display": display,
                "options": options if options else [],
            }
        return result


class DisplayToJsonMapper:
    def map(self, display_settings: dict) -> dict:
        """Convert display settings back to JSON format"""
        result = {}
        for display_name, display_value in display_settings.items():
            if display_name not in SETTINGS_FIELDS:
                continue

            field_info = SETTINGS_FIELDS[display_name]
            json_field = field_info["json_field"]
            options = field_info.get("options", [])
            field_type = field_info["type"]

            if field_type == "bool":
                result[json_field] = display_value == "是"
            elif field_type in ("int", "str") and options:
                try:
                    idx = options.index(display_value)
                    result[json_field] = idx
                except ValueError:
                    result[json_field] = display_value
            else:
                if field_type == "float":
                    result[json_field] = float(display_value)
                elif field_type == "int":
                    result[json_field] = int(display_value)
                else:
                    result[json_field] = display_value
        return result
