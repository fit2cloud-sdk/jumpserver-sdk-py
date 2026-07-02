from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from . import IDDisplay, IDName, LabelValue


@dataclass
class Phone:
    code: str = ""
    phone: Any = None


@dataclass
class MfaLevel:
    value: int = 0
    label: str = ""


@dataclass
class User:
    id: str = ""
    name: str = ""
    username: str = ""
    email: str = ""
    wechat: str = ""
    phone: Optional[Phone] = None
    mfa_level: Optional[MfaLevel] = None
    source: Optional[LabelValue] = None
    wecom_id: str = ""
    dingtalk_id: str = ""
    feishu_id: str = ""
    lark_id: str = ""
    slack_id: str = ""
    created_by: str = ""
    updated_by: str = ""
    comment: str = ""
    avatar_url: str = ""
    groups: list[IDName] = field(default_factory=list)
    system_roles: list[IDDisplay] = field(default_factory=list)
    org_roles: list[IDDisplay] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    password_strategy: Optional[LabelValue] = None
    is_superuser: bool = False
    is_org_admin: bool = False
    is_service_account: bool = False
    is_valid: bool = False
    is_expired: bool = False
    is_active: bool = False
    is_otp_secret_key_bound: bool = False
    can_public_key_auth: bool = False
    mfa_enabled: bool = False
    need_update_password: bool = False
    mfa_force_enabled: bool = False
    is_first_login: bool = False
    login_blocked: bool = False
    date_expired: str = ""
    date_joined: str = ""
    last_login: str = ""
    date_updated: str = ""
    date_api_key_last_used: str = ""
    date_password_last_updated: str = ""
    orgs_roles: Optional[dict[str, list[str]]] = None


@dataclass
class UserRequest:
    name: str = ""
    username: str = ""
    email: str = ""
    groups: list[str] = field(default_factory=list)
    password_strategy: str = ""
    need_update_password: bool = False
    mfa_level: int = 0
    source: str = "local"
    system_roles: list[str] = field(default_factory=list)
    org_roles: list[str] = field(default_factory=list)
    is_active: bool = True
    date_expired: str = ""
    phone: str = ""
    password: str = ""
    comment: str = ""


@dataclass
class Group:
    id: str = ""
    name: str = ""
    comment: str = ""
    users: list[str] = field(default_factory=list)
    org_id: str = ""
    org_name: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class GroupRequest:
    name: str = ""
    comment: str = ""
    users: list[str] = field(default_factory=list)


@dataclass
class UserGroupRelation:
    user: str = ""
    usergroup: str = ""
    org_id: str = ""
