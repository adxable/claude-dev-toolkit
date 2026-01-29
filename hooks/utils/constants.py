#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Constants for Claude Code Hooks.
"""

import os
from pathlib import Path

# Base directory for all logs
# Default is 'logs' in the current working directory
LOG_BASE_DIR = os.environ.get("CLAUDE_HOOKS_LOG_DIR", "logs")

def get_session_log_dir(session_id: str) -> Path:
    """
    Get the log directory for a specific session.

    Args:
        session_id: The Claude session ID

    Returns:
        Path object for the session's log directory
    """
    return Path(LOG_BASE_DIR) / session_id

def ensure_session_log_dir(session_id: str) -> Path:
    """
    Ensure the log directory for a session exists.

    Args:
        session_id: The Claude session ID

    Returns:
        Path object for the session's log directory
    """
    log_dir = get_session_log_dir(session_id)
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_memory_dir() -> Path:
    """Get the memory/ directory relative to the toolkit root."""
    # hooks/utils/constants.py -> hooks/utils -> hooks -> toolkit root
    root = Path(__file__).resolve().parent.parent.parent
    d = root / "memory"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_knowledge_dir() -> Path:
    """Get the shared knowledge directory (memory/knowledge/)."""
    d = get_memory_dir() / "knowledge"
    d.mkdir(parents=True, exist_ok=True)
    (d / "fragments").mkdir(parents=True, exist_ok=True)
    return d


def get_local_dir() -> Path:
    """Get the personal/local knowledge directory (memory/local/)."""
    d = get_memory_dir() / "local"
    d.mkdir(parents=True, exist_ok=True)
    (d / "fragments").mkdir(parents=True, exist_ok=True)
    return d
