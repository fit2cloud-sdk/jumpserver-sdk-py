"""JumpServer SDK - Utility helpers."""

from typing import Any, Optional


def build_url(path: str, params: Optional[dict[str, Any]] = None) -> str:
    """Append query parameters to a URL path."""
    if not params:
        return path
    filtered = {k: v for k, v in params.items() if v is not None and v != ""}
    if not filtered:
        return path
    parts = []
    for k, v in filtered.items():
        parts.append(f"{k}={_quote(str(v))}")
    qs = "&".join(parts)
    if "?" in path:
        return f"{path}&{qs}"
    return f"{path}?{qs}"


def _quote(s: str) -> str:
    """Minimal URL quoting (avoids urllib.parse for simplicity)."""
    import re

    return re.sub(r"[^a-zA-Z0-9_.~\-]", lambda m: f"%{ord(m.group(0)):02X}", s)


def format_path(tpl: str, *args: Any) -> str:
    """Format a path template, e.g. '/api/v1/users/users/%s/' % user_id."""
    return tpl % args
