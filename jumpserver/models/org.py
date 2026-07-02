from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Organization:
    id: str = ""
    name: str = ""
    is_root: bool = False
    is_default: bool = False
    members: list[str] = field(default_factory=list)
    comment: str = ""
    date_created: str = ""
    date_updated: str = ""
    created_by: str = ""


@dataclass
class OrganizationRequest:
    name: str = ""
    members: list[str] = field(default_factory=list)
    comment: str = ""
