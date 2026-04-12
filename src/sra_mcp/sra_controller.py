"""SRA process controller - handles SRA.exe and SRA-cli.exe operations"""
import subprocess
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


class SRAProcessError(Exception):
    """Raised when SRA process operation fails"""
    pass


class SRAAlreadyRunningError(SRAProcessError):
    """Raised when SRA is already running"""
    pass


class SRATimeoutError(SRAProcessError):
    """Raised when task execution times out"""
    pass


class SRAConfigNotFoundError(SRAProcessError):
    """Raised when config file is not found"""
    pass


@dataclass
class TaskResult:
    """Result of a task execution"""
    success: bool
    message: str
    output: str = ""


def _is_admin() -> bool:
    """Check if current process is running with administrator privileges."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def _run_as_admin(exe_path: str, args: str = "", cwd: str = "") -> bool:
    """Run a process with administrator privileges using ShellExecuteEx.

    If already running as admin, no UAC prompt will be shown.
    Otherwise, this will trigger a UAC prompt on Windows.
    Returns True if the process was started successfully.
    """
    if sys.platform != "win32":
        return False

    try:
        import ctypes
        from ctypes import wintypes

        SW_SHOWNORMAL = 1

        class SHELLEXECUTEINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("fMask", wintypes.ULONG),
                ("hwnd", wintypes.HWND),
                ("lpVerb", wintypes.LPCWSTR),
                ("lpFile", wintypes.LPCWSTR),
                ("lpParameters", wintypes.LPCWSTR),
                ("lpDirectory", wintypes.LPCWSTR),
                ("nShow", ctypes.c_int),
                ("hInstApp", wintypes.HINSTANCE),
                ("lpIDList", ctypes.c_void_p),
                ("lpClass", wintypes.LPCWSTR),
                ("hkeyClass", wintypes.HKEY),
                ("dwHotKey", wintypes.DWORD),
                ("hIcon", wintypes.HANDLE),
                ("hProcess", wintypes.HANDLE),
            ]

        SEE_MASK_NOCLOSEPROCESS = 0x00000040
        SEE_MASK_UNICODE = 0x00004000
        SEE_MASK_NO_CONSOLE = 0x00008000

        sei = SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
        sei.fMask = SEE_MASK_NOCLOSEPROCESS | SEE_MASK_UNICODE | SEE_MASK_NO_CONSOLE
        sei.lpVerb = "runas"
        sei.lpFile = exe_path
        sei.lpParameters = args
        sei.lpDirectory = cwd
        sei.nShow = SW_SHOWNORMAL

        result = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))
        return result > 32  # > 32 indicates success
    except Exception:
        return False


class SRAController:
    """Controller for SRA GUI and CLI operations"""

    def __init__(self, sra_path: str | Path):
        self.sra_path = Path(sra_path)
        self.sra_exe = self.sra_path / "SRA.exe"
        self.cli_exe = self.sra_path / "SRA-cli.exe"

    def _is_process_running(self, process_name: str) -> bool:
        """Check if a process with given name is running"""
        try:
            import psutil
            for proc in psutil.process_iter(["name"]):
                if proc.info["name"] == process_name:
                    return True
            return False
        except ImportError:
            # Fallback: use tasklist
            result = subprocess.run(
                ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                capture_output=True, text=True
            )
            return process_name in result.stdout

    def is_running(self) -> bool:
        """Check if SRA is currently running"""
        return self._is_process_running("SRA.exe")

    def check_sra_exists(self) -> bool:
        """Check if SRA.exe exists"""
        return self.sra_exe.exists()

    def check_cli_exists(self) -> bool:
        """Check if SRA-cli.exe exists"""
        return self.cli_exe.exists()

    def start_gui(self, admin: bool = True) -> bool:
        """Start SRA GUI application.

        Args:
            admin: If True, request administrator privileges.
                   If already running as admin, no UAC prompt will be shown.
        """
        if not self.check_sra_exists():
            raise SRAProcessError(f"SRA.exe not found at {self.sra_exe}")

        if self.is_running():
            raise SRAAlreadyRunningError("SRA is already running")

        try:
            if admin:
                if _is_admin():
                    # Already running as admin, use subprocess directly
                    subprocess.Popen(
                        [str(self.sra_exe)],
                        cwd=str(self.sra_path),
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    # Use ShellExecuteEx with runas to request admin privileges
                    success = _run_as_admin(
                        str(self.sra_exe),
                        cwd=str(self.sra_path)
                    )
                    if not success:
                        raise SRAProcessError("Failed to elevate to admin privileges")
            else:
                subprocess.Popen(
                    [str(self.sra_exe)],
                    cwd=str(self.sra_path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            return True
        except Exception as e:
            raise SRAProcessError(f"Failed to start SRA: {e}")

    def run_task(
        self,
        config_name: str,
        task_name: Optional[str] = None,
        timeout: int = 1800,
        admin: bool = False
    ) -> TaskResult:
        """Run a task using SRA-cli.exe.

        Args:
            config_name: Name of the config to use.
            task_name: Optional specific task name.
            timeout: Timeout in seconds.
            admin: If True, request administrator privileges.
        """
        if not self.check_cli_exists():
            raise SRAProcessError(f"SRA-cli.exe not found at {self.cli_exe}")

        # Build command: SRA-cli.exe -e "run <config>" or SRA-cli.exe -e "single <task> <config>"
        if task_name:
            cmd_str = f"single {task_name} {config_name}"
        else:
            cmd_str = f"run {config_name}"

        # If admin privileges are requested and current process is not admin,
        # use ShellExecuteEx with runas to elevate
        if admin and not _is_admin():
            # Use ShellExecuteEx with runas to request admin privileges
            # Note: ShellExecuteEx cannot capture stdout/stderr
            full_args = f'-e "{cmd_str}" --inline'
            success = _run_as_admin(
                str(self.cli_exe),
                args=full_args,
                cwd=str(self.sra_path)
            )
            if success:
                return TaskResult(
                    success=True,
                    message="Task launched with admin privileges.",
                    output=""
                )
            else:
                return TaskResult(
                    success=False,
                    message="Failed to elevate to admin privileges. Please run the MCP server as administrator, or use sra_start() first.",
                    output=""
                )

        # Use subprocess.run() with PIPE to capture output for debugging
        # The output will be printed and also returned in TaskResult
        try:
            # Set PYTHONIOENCODING=utf-8 to avoid GBK encoding errors on Chinese Windows
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            result = subprocess.run(
                [str(self.cli_exe), "-e", cmd_str, "--inline"],
                cwd=str(self.sra_path),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                env=env
            )
            # Decode and print output for debugging
            output = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            if output:
                print(f"===== SRA-cli output start =====\n{output}\n===== SRA-cli output end =====", flush=True)
            success = result.returncode == 0
            return TaskResult(
                success=success,
                message="Task completed successfully" if success else f"Task failed with exit code {result.returncode}",
                output=output
            )
        except subprocess.TimeoutExpired:
            raise SRATimeoutError(f"Task timed out after {timeout} seconds")
        except OSError as e:
            if e.winerror == 740:  # ERROR_PRIVILEGE_NOT_HELD
                return TaskResult(
                    success=False,
                    message="SRA-cli.exe requires administrator privileges. Please run the MCP server as administrator.",
                    output=""
                )
            raise SRAProcessError(f"Failed to run task: {e}")
        except Exception as e:
            raise SRAProcessError(f"Failed to run task: {e}")