"""Tests for sra_controller.py"""
import pytest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path

from sra_mcp.sra_controller import (
    SRAController,
    SRAProcessError,
    SRAAlreadyRunningError,
    SRATimeoutError,
    SRAConfigNotFoundError,
    TaskResult,
)


@pytest.fixture
def controller(tmp_path):
    """Create a controller with temp path."""
    return SRAController(tmp_path)


class TestIsRunning:
    def test_sra_not_running_check(self, controller):
        """Test checking if SRA is not running."""
        with patch.object(controller, '_is_process_running', return_value=False):
            assert controller.is_running() is False


class TestStartGUI:
    def test_start_sra_without_exe(self, controller):
        """Test that SRAProcessError is raised when SRA.exe does not exist."""
        with patch.object(controller, 'check_sra_exists', return_value=False):
            with pytest.raises(SRAProcessError) as exc_info:
                controller.start_gui()
            assert "SRA.exe not found" in str(exc_info.value)

    def test_start_sra_already_running(self, controller):
        """Test that SRAAlreadyRunningError is raised when SRA is already running."""
        with patch.object(controller, 'check_sra_exists', return_value=True):
            with patch.object(controller, 'is_running', return_value=True):
                with pytest.raises(SRAAlreadyRunningError) as exc_info:
                    controller.start_gui()
                assert "already running" in str(exc_info.value)

    def test_start_sra_success(self, controller):
        """Test successful SRA GUI start."""
        with patch.object(controller, 'check_sra_exists', return_value=True):
            with patch.object(controller, 'is_running', return_value=False):
                with patch('subprocess.Popen') as mock_popen:
                    with patch('sra_mcp.sra_controller._is_admin', return_value=True):
                        result = controller.start_gui()
                        assert result is True
                        mock_popen.assert_called_once()


class TestRunTask:
    def test_run_task_cli_not_found(self, controller):
        """Test that SRAProcessError is raised when SRA-cli.exe does not exist."""
        with patch.object(controller, 'check_cli_exists', return_value=False):
            with pytest.raises(SRAProcessError) as exc_info:
                controller.run_task("config.yaml")
            assert "SRA-cli.exe not found" in str(exc_info.value)

    def test_run_task_success(self, controller):
        """Test successful task execution."""
        with patch.object(controller, 'check_cli_exists', return_value=True):
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = b"output"
                mock_result.stderr = b""
                mock_run.return_value = mock_result

                result = controller.run_task("config.yaml")

                assert result.success is True
                assert result.message == "Task completed successfully"
                mock_run.assert_called_once()

    def test_run_task_with_task_name(self, controller):
        """Test running a specific task."""
        with patch.object(controller, 'check_cli_exists', return_value=True):
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = b"task output"
                mock_result.stderr = b""
                mock_run.return_value = mock_result

                result = controller.run_task("config.yaml", task_name="my_task")

                assert result.success is True
                mock_run.assert_called_once()
                args = mock_run.call_args[0][0]
                assert "single my_task config.yaml" in " ".join(args)

    def test_run_task_failure(self, controller):
        """Test task execution failure."""
        with patch.object(controller, 'check_cli_exists', return_value=True):
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 1
                mock_result.stdout = b""
                mock_result.stderr = b"error"
                mock_run.return_value = mock_result

                result = controller.run_task("config.yaml")

                assert result.success is False
                assert result.message == "Task failed with exit code 1"

    def test_run_task_timeout(self, controller):
        """Test task timeout."""
        import subprocess
        with patch.object(controller, 'check_cli_exists', return_value=True):
            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired("cmd", 1800)

                with pytest.raises(SRATimeoutError) as exc_info:
                    controller.run_task("config.yaml")
                assert "timed out" in str(exc_info.value)


class TestCheckExists:
    def test_check_sra_exists(self, controller):
        """Test checking if SRA.exe exists."""
        with patch('pathlib.Path.exists', return_value=True):
            assert controller.check_sra_exists() is True

    def test_check_cli_exists(self, controller):
        """Test checking if SRA-cli.exe exists."""
        with patch('pathlib.Path.exists', return_value=True):
            assert controller.check_cli_exists() is True


class TestTaskResult:
    def test_task_result_creation(self):
        """Test TaskResult dataclass."""
        result = TaskResult(success=True, message="OK", output="data")
        assert result.success is True
        assert result.message == "OK"
        assert result.output == "data"

    def test_task_result_default_output(self):
        """Test TaskResult with default output."""
        result = TaskResult(success=False, message="Failed")
        assert result.output == ""