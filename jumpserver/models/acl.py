from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Role:
    id: str = ""
    name: str = ""
    scope: Any = None
    display_name: str = ""
    comment: str = ""
    builtin: bool = False
    date_created: str = ""
    date_updated: str = ""


@dataclass
class Label:
    id: str = ""
    name: str = ""
    value: str = ""
    display_name: str = ""
    comment: str = ""
    org_id: str = ""
    org_name: str = ""
    date_created: str = ""
    date_updated: str = ""
    res_amount: int = 0


@dataclass
class LabelRequest:
    name: str = ""
    value: str = ""
    comment: str = ""


@dataclass
class CommandFilter:
    id: str = ""
    name: str = ""
    command_groups: Any = None
    accounts: Any = None
    users: Any = None
    user_groups: Any = None
    assets: Any = None
    nodes: Any = None
    action: Any = None
    is_active: bool = False
    priority: int = 0
    comment: str = ""
    org_id: str = ""
    org_name: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class CommandFilterRequest:
    name: str = ""
    command_groups: Any = None
    accounts: Any = None
    users: Any = None
    user_groups: Any = None
    assets: Any = None
    nodes: Any = None
    action: str = "reject"
    is_active: bool = True
    priority: int = 50
    comment: str = ""


@dataclass
class CommandGroup:
    id: str = ""
    name: str = ""
    type: Any = None
    content: str = ""
    comment: str = ""
    org_id: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class CommandGroupRequest:
    name: str = ""
    type: Any = None
    content: str = ""
    comment: str = ""


@dataclass
class LoginACL:
    id: str = ""
    name: str = ""
    action: Any = None
    is_active: bool = False
    priority: int = 0
    comment: str = ""
    date_created: str = ""
    date_updated: str = ""
