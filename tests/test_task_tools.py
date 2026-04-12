"""Tests for task MCP tools"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from sra_mcp.tools.task import (
    start_sra,
    run_task,
    TaskToolError,
)
from sra_mcp.sra_controller import (
    SRAController,
    SRAProcessError,
    SRAAlreadyRunningError,
    SRATimeoutError,
    SRAConfigNotFoundError,
    TaskResult,
)
from sra_mcp.config import SRAConfig


class TestStartSRA:
    """Tests for start_sra function"""

    def test_start_sra_success(self):
        """Test successful SRA startup"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller

                result = start_sra()

                mock_controller.start_gui.assert_called_once()
                assert result["success"] is True
                assert result["message"] == "SRA started successfully"

    def test_start_sra_with_config(self):
        """Test start_sra with explicit config"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")

        with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller

            result = start_sra(config=mock_config)

            mock_controller.start_gui.assert_called_once()
            assert result["success"] is True

    def test_start_sra_already_running(self):
        """Test when SRA is already running"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller
                mock_controller.start_gui.side_effect = SRAAlreadyRunningError("SRA is already running")

                result = start_sra()

                assert result["success"] is False
                assert result["message"] == "SRA is already running"

    def test_start_sra_process_error(self):
        """Test process error during startup"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller
                mock_controller.start_gui.side_effect = SRAProcessError("Failed to start SRA: access denied")

                result = start_sra()

                assert result["success"] is False
                assert result["message"] == "Failed to start SRA: access denied"


class TestRunTask:
    """Tests for run_task function"""

    def test_run_task_success(self):
        """Test successful task execution"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")
        mock_config.get_configs_dir.return_value = Path("/mock/configs")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller
                mock_controller.run_task.return_value = TaskResult(
                    success=True,
                    message="Task completed successfully",
                    output="task output here"
                )

                with patch.object(Path, "exists", return_value=True):
                    result = run_task(config_name="test_config")

                assert result["success"] is True
                assert result["message"] == "Task completed successfully"
                assert result["output"] == "task output here"
                mock_controller.run_task.assert_called_once_with(
                    config_name="test_config",
                    task_name=None,
                    timeout=1800,
                    admin=False
                )

    def test_run_task_with_task_name(self):
        """Test run_task with explicit task name"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")
        mock_config.get_configs_dir.return_value = Path("/mock/configs")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller
                mock_controller.run_task.return_value = TaskResult(
                    success=True,
                    message="Task completed successfully",
                    output=""
                )

                with patch.object(Path, "exists", return_value=True):
                    result = run_task(config_name="test_config", task_name="specific_task")

                mock_controller.run_task.assert_called_once_with(
                    config_name="test_config",
                    task_name="specific_task",
                    timeout=1800,
                    admin=False
                )

    def test_run_task_timeout(self):
        """Test task timeout"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")
        mock_config.get_configs_dir.return_value = Path("/mock/configs")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller
                mock_controller.run_task.side_effect = SRATimeoutError("Task timed out after 1800 seconds")

                with patch.object(Path, "exists", return_value=True):
                    result = run_task(config_name="test_config", timeout=1800)

                assert result["success"] is False
                assert "timed out" in result["message"]
                assert result["output"] == ""

    def test_run_task_process_error(self):
        """Test task execution failure"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")
        mock_config.get_configs_dir.return_value = Path("/mock/configs")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch("sra_mcp.tools.task.SRAController") as mock_controller_class:
                mock_controller = MagicMock()
                mock_controller_class.return_value = mock_controller
                mock_controller.run_task.side_effect = SRAProcessError("Task execution failed: cli not found")

                with patch.object(Path, "exists", return_value=True):
                    result = run_task(config_name="test_config")

                assert result["success"] is False
                assert "failed" in result["message"]
                assert result["output"] == ""

    def test_run_task_config_not_found(self):
        """Test config file not found"""
        mock_config = MagicMock(spec=SRAConfig)
        mock_config.sra_path = Path("/mock/sra/path")
        mock_config.get_configs_dir.return_value = Path("/mock/configs")

        with patch("sra_mcp.tools.task.SRAConfig") as mock_config_class:
            mock_config_class.load.return_value = mock_config

            with patch.object(Path, "exists", return_value=False):
                with pytest.raises(SRAConfigNotFoundError) as exc_info:
                    run_task(config_name="nonexistent_config")

                assert "not found" in str(exc_info.value)


class TestTaskToolError:
    """Tests for TaskToolError exception class"""

    def test_task_tool_error_inheritance(self):
        """Test TaskToolError is an Exception"""
        assert issubclass(TaskToolError, Exception)

    def test_task_tool_error_message(self):
        """Test TaskToolError can hold a message"""
        error = TaskToolError("Test error message")
        assert str(error) == "Test error message"