from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = [
    "Session", "Command", "FTPLog", "LoginLog", "OperateLog",
]


@dataclass
class Session:
    id: str = ""
    user: str = ""
    asset: str = ""
    account: str = ""
    protocol: str = ""
    type: Any = None
    login_from: Any = None
    remote_addr: str = ""
    is_finished: bool = False
    is_success: bool = False
    org_id: str = ""
    date_start: str = ""
    date_end: str = ""


@dataclass
class Command:
    id: str = ""
    user: str = ""
    asset: str = ""
    account: str = ""
    session: str = ""
    input: str = ""
    output: str = ""
    risk_level: int = 0
    org_id: str = ""
    timestamp: int = 0


@dataclass
class FTPLog:
    id: str = ""
    user: str = ""
    asset: str = ""
    account: str = ""
    session: str = ""
    remote_addr: str = ""
    operate: Any = None
    path: str = ""
    is_success: bool = False
    org_id: str = ""
    date_start: str = ""


@dataclass
class LoginLog:
    id: Any = None
    username: str = ""
    type: Any = None
    ip: str = ""
    city: str = ""
    user_agent: str = ""
    mfa: Any = None
    status: Any = None
    backend: str = ""
    reason: str = ""
    datetime: str = ""


@dataclass
class OperateLog:
    id: Any = None
    user: str = ""
    action: Any = None
    resource_type: str = ""
    resource: str = ""
    remote_addr: str = ""
    datetime: str = ""
