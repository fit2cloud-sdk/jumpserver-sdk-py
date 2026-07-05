from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from . import LabelValue

__all__ = [
    "Account", "AccountRequest",
    "AccountTemplate", "AccountTemplateRequest", "AccountBulkByTemplateRequest",
    "ChangeSecretAutomation", "ChangeSecretAutomationRequest",
    "AccountBackupPlan", "AccountBackupPlanRequest",
    "AccountVerifyResult", "AccountVerifyTaskRequest", "AccountVerifyTask",
]


@dataclass
class Account:
    id: str = ""
    name: str = ""
    username: str = ""
    asset: Any = None
    secret_type: Optional[LabelValue] = None
    secret: str = ""
    privileged: bool = False
    is_active: bool = False
    connectivity: Any = None
    su_from: Any = None
    version: int = 0
    comment: str = ""
    created_by: str = ""
    updated_by: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class AccountRequest:
    name: str = ""
    username: str = ""
    asset: str = ""
    secret_type: str = "password"
    secret: str = ""
    push_now: bool = False
    privileged: bool = False
    is_active: bool = True
    su_from: str = ""
    comment: str = ""


@dataclass
class AccountTemplate:
    id: str = ""
    name: str = ""
    username: str = ""
    secret_type: Any = None
    secret: str = ""
    privileged: bool = False
    is_active: bool = False
    su_from: Any = None
    auto_push: bool = False
    push_params: Any = None
    org_id: str = ""
    org_name: str = ""
    comment: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class AccountTemplateRequest:
    name: str = ""
    username: str = ""
    secret_type: str = "password"
    secret: str = ""
    privileged: bool = False
    is_active: bool = True
    su_from: str = ""
    auto_push: bool = False
    comment: str = ""


@dataclass
class AccountBulkByTemplateRequest:
    assets: list[str] = field(default_factory=list)
    template: str = ""
    on_invalid: str = ""
    is_active: bool = True


@dataclass
class ChangeSecretAutomation:
    id: str = ""
    name: str = ""
    accounts: list[Any] = field(default_factory=list)
    assets: list[Any] = field(default_factory=list)
    nodes: list[Any] = field(default_factory=list)
    secret_type: Any = None
    secret_strategy: Any = None
    is_active: bool = False
    is_periodic: bool = False
    crontab: str = ""
    interval: int = 0
    recipients: list[Any] = field(default_factory=list)
    org_id: str = ""
    org_name: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class ChangeSecretAutomationRequest:
    name: str = ""
    accounts: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    secret_type: str = "password"
    secret_strategy: str = ""
    is_active: bool = True
    is_periodic: bool = False
    crontab: str = ""
    interval: int = 0
    recipients: list[str] = field(default_factory=list)
    comment: str = ""


@dataclass
class AccountBackupPlan:
    id: str = ""
    name: str = ""
    accounts: list[Any] = field(default_factory=list)
    assets: list[Any] = field(default_factory=list)
    nodes: list[Any] = field(default_factory=list)
    secret_type: Any = None
    secret_strategy: Any = None
    is_active: bool = False
    is_periodic: bool = False
    crontab: str = ""
    interval: int = 0
    recipients: list[Any] = field(default_factory=list)
    backup_type: Any = None
    org_id: str = ""
    org_name: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class AccountBackupPlanRequest:
    name: str = ""
    accounts: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    secret_type: str = "password"
    secret_strategy: str = ""
    is_active: bool = True
    is_periodic: bool = False
    crontab: str = ""
    interval: int = 0
    recipients: list[str] = field(default_factory=list)
    comment: str = ""


@dataclass
class AccountVerifyResult:
    account: str = ""
    asset: str = ""
    is_valid: bool = False
    connectivity: str = ""
    error: str = ""
    date_verified: str = ""


@dataclass
class AccountVerifyTaskRequest:
    accounts: list[str] = field(default_factory=list)


@dataclass
class AccountVerifyTask:
    task: str = ""
