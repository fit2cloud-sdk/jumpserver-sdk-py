from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "Role", "Label", "LabelRequest",
    "CommandFilter", "CommandFilterRequest",
    "CommandGroup", "CommandGroupRequest",
    "LoginACL",
]


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
    """Request payload for creating/updating a command filter.

    Field formats (based on real API responses)::

        users/assets/user_groups/nodes::
            {"type": "all"}
            {"type": "ids", "ids": ["<uuid>", ...]}
            {"type": "attrs", "attrs": [{"name": "...", "match": "...", "value": ...}]}

        accounts:           ["@ALL"]  or  ["@SPEC", "<username>", ...]
        command_groups:     ["<uuid>", ...]
        reviewers:          ["<uuid>", ...]

        action: one of "reject", "accept", "review", "warning", "notify_and_warn"
    """

    name: str = ""
    command_groups: list[str] = field(default_factory=list)
    accounts: list[str] = field(default_factory=list)
    users: Any = None
    user_groups: Any = None
    assets: Any = None
    nodes: Any = None
    reviewers: list[str] = field(default_factory=list)
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
