"""JumpServer SDK - Utility helpers."""

from typing import Any


def format_path(tpl: str, *args: Any) -> str:
    """Format a path template, e.g. '/api/v1/users/users/%s/' % user_id."""
    return tpl % args


__all__ = ["format_path"]
