"""SRA MCP Configuration"""
import json
import os
from pathlib import Path
from dataclasses import dataclass


class ConfigNotFoundError(Exception):
    """Raised when config.json is not found"""
    pass


class ConfigReadError(Exception):
    """Raised when config.json cannot be read"""
    pass


@dataclass
class SRAConfig:
    sra_path: str

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "SRAConfig":
        """
        Load configuration from config.json.

        config.json must be in the same directory as this module (src/sra_mcp/).
        """
        # 拼接路径
        if config_path is None:
            module_dir = Path(__file__).parent
            config_path = module_dir / "config.json"
        else:
            config_path = Path(config_path)

        if not config_path.exists():
            raise ConfigNotFoundError(
                "config.json not found. Create it in the MCP directory"
            )
        # 打开文件
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise ConfigNotFoundError(f"Config file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ConfigReadError(f"Invalid JSON in config file: {e}")
        return cls(sra_path=data.get("sra_path", ""))

    def get_sra_exe_path(self) -> Path:
        return Path(self.sra_path) / "SRA.exe"

    def get_sra_cli_exe_path(self) -> Path:
        return Path(self.sra_path) / "SRA-cli.exe"

    def get_settings_path(self) -> Path:
        appdata = Path(os.environ.get("APPDATA", ""))
        return appdata / "SRA" / "settings.json"

    def get_configs_dir(self) -> Path:
        appdata = Path(os.environ.get("APPDATA", ""))
        return appdata / "SRA" / "configs"