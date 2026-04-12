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

        Search order:
        1. Explicit config_path argument
        2. SRA_MCP_CONFIG environment variable
        3. {module directory}/config.json
        4. {module directory}/../config.json
        5. ./config.json (current working directory)
        6. ../config.json (parent directory)
        """
        if config_path is None:
            config_path = os.environ.get("SRA_MCP_CONFIG")

        if config_path is None:
            # Search relative to this module file's directory
            # Module is at src/sra_mcp/config.py, config.json is at SRA_MCP/config.json
            module_dir = Path(__file__).parent
            project_root = module_dir.parent.parent
            search_paths = [
                project_root / "config.json",  # SRA_MCP/config.json
                module_dir / "config.json",
                module_dir.parent / "config.json",
                Path.cwd() / "config.json",
                Path.cwd().parent / "config.json",
            ]
            for p in search_paths:
                if p.exists():
                    config_path = p
                    break

        if config_path is None:
            raise ConfigNotFoundError(
                "config.json not found. Create it in the MCP directory or set SRA_MCP_CONFIG environment variable."
            )

        config_path = Path(config_path)
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