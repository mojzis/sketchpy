"""Tests for the server process management."""

import os
import signal
import subprocess
import time
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent
PID_FILE = PROJECT_ROOT / 'logs' / 'srv.pid'


def cleanup_server():
    """Helper to ensure server is stopped."""
    if PID_FILE.exists():
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.5)
                # Force kill if still running
                try:
                    os.kill(pid, 0)  # Check if process exists
                    os.kill(pid, signal.SIGKILL)
                    time.sleep(0.2)
                except OSError:
                    pass
            except (OSError, ProcessLookupError):
                pass
        except (ValueError, FileNotFoundError):
            pass
        finally:
            if PID_FILE.exists():
                PID_FILE.unlink()


@pytest.fixture(autouse=True)
def ensure_server_stopped():
    """Ensure server is stopped before and after each test."""
    cleanup_server()
    yield
    cleanup_server()


def test_server_auto_restart():
    """Test that starting the server automatically kills an existing server."""
    # Start first server instance in background
    result1 = subprocess.run(
        ['uv', 'run', 'srv', '--background'],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result1.returncode == 0, f"First server failed to start: {result1.stderr}"

    # Give it time to start and complete initial build (can take 3-4 seconds)
    time.sleep(5)

    # Check that PID file was created
    assert PID_FILE.exists(), "PID file was not created"

    # Read first PID
    with open(PID_FILE, 'r') as f:
        first_pid = int(f.read().strip())

    # Verify first process is running
    try:
        os.kill(first_pid, 0)  # Signal 0 just checks if process exists
        first_process_running = True
    except OSError:
        first_process_running = False

    assert first_process_running, f"First server process (PID {first_pid}) not running"

    # Start second server instance (should kill first one)
    result2 = subprocess.run(
        ['uv', 'run', 'srv', '--background'],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result2.returncode == 0, f"Second server failed to start: {result2.stderr}"

    # Give it time to kill old server and start new one
    time.sleep(2)

    # Check that PID file still exists with a new PID
    assert PID_FILE.exists(), "PID file was not created for second server"

    # Read second PID
    with open(PID_FILE, 'r') as f:
        second_pid = int(f.read().strip())

    # Verify PIDs are different
    assert first_pid != second_pid, "PIDs should be different after restart"

    # Verify first process is no longer running
    try:
        os.kill(first_pid, 0)
        first_still_running = True
    except OSError:
        first_still_running = False

    assert not first_still_running, f"First server (PID {first_pid}) should have been killed"

    # Verify second process is running
    try:
        os.kill(second_pid, 0)
        second_process_running = True
    except OSError:
        second_process_running = False

    assert second_process_running, f"Second server process (PID {second_pid}) not running"


def test_server_pid_file_management():
    """Test that PID file is properly created and cleaned up."""
    # Ensure no PID file exists
    if PID_FILE.exists():
        PID_FILE.unlink()

    # Start server
    result = subprocess.run(
        ['uv', 'run', 'srv', '--background'],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=10
    )

    assert result.returncode == 0, f"Server failed to start: {result.stderr}"

    # Give it time to start
    time.sleep(2)

    # Check PID file exists
    assert PID_FILE.exists(), "PID file should exist after server starts"

    # Read PID and verify it's a valid integer
    with open(PID_FILE, 'r') as f:
        pid_content = f.read().strip()

    try:
        pid = int(pid_content)
    except ValueError:
        pytest.fail(f"PID file contains invalid content: {pid_content}")

    # Verify process exists
    try:
        os.kill(pid, 0)
        process_exists = True
    except OSError:
        process_exists = False

    assert process_exists, f"Process with PID {pid} from PID file is not running"
