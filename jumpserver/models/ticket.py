from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Ticket:
    id: str = ""
    serial_num: str = ""
    type: Any = None
    state: Any = None
    status: Any = None
    title: str = ""
    comment: str = ""
    org_id: str = ""
    org_name: str = ""
    applicant: Any = None
    date_created: str = ""
    date_updated: str = ""


@dataclass
class TicketRequest:
    type: str = "general"
    title: str = ""
    apply_accounts: list[str] = field(default_factory=list)
    apply_assets: list[str] = field(default_factory=list)
    apply_nodes: list[str] = field(default_factory=list)
    apply_actions: list[str] = field(default_factory=list)
    apply_date_start: str = ""
    apply_date_expired: str = ""
    comment: str = ""


@dataclass
class TicketFlow:
    id: str = ""
    type: Any = None
    approve_strategy: Any = None
    applicants: list[dict] = field(default_factory=list)
    is_active: bool = False
    date_created: str = ""
    date_updated: str = ""
    created_by: str = ""
    org_id: str = ""
    org_name: str = ""
    comment: str = ""


@dataclass
class TicketFlowRequest:
    approve_strategy: Any = None
    applicants: list[str] = field(default_factory=list)
    is_active: bool = True
    comment: str = ""
