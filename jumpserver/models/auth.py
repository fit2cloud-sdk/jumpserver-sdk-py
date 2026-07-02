from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TokenRequest:
    username: str = ""
    password: str = ""
    mfa_type: str = ""
    mfa_code: str = ""


@dataclass
class Token:
    token: str = ""
    keyword: str = ""
    date_expired: str = ""
    user: Any = None


@dataclass
class ConnectionTokenRequest:
    user: str = ""
    asset: str = ""
    account: str = ""
    protocol: str = ""
    connect_method: str = ""
    input_username: str = ""
    input_secret: str = ""
    connect_options: Any = None


@dataclass
class ConnectionToken:
    id: str = ""
    value: str = ""
    user: Any = None
    asset: Any = None
    account: Any = None
    protocol: str = ""
    expire_at: int = 0
    is_active: bool = False
    org_name: str = ""
    date_created: str = ""


@dataclass
class SSOLoginRequest:
    username: str = ""
    next: str = ""
