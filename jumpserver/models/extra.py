from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import LabelValue


@dataclass
class PublicSetting:
    interface: Any = None
    enable_watermark: bool = False
    security_command_execution: bool = False
    xpack_license_is_valid: bool = False


@dataclass
class SettingItem:
    name: str = ""
    value: Any = None
    category: str = ""
    encrypted: bool = False


@dataclass
class License:
    is_valid: bool = False
    edition: str = ""
    expired_date: str = ""
    count: int = 0
    corporation: str = ""


@dataclass
class OpsJobRequest:
    assets: list[str] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    module: str = "shell"
    args: str = ""
    run_as: str = ""
    run_as_policy: str = "skip"
    instant: bool = True
    is_periodic: bool = False
    timeout: int = 60


@dataclass
class OpsJobResponse:
    task_id: str = ""


@dataclass
class OpsJobResultSummary:
    ok: list[str] = field(default_factory=list)
    dark: dict[str, Any] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)
    failures: dict[str, Any] = field(default_factory=dict)


@dataclass
class OpsJobResult:
    status: Any = None
    is_finished: bool = False
    is_success: bool = False
    time_cost: float = 0.0
    job_id: str = ""
    summary: Any = None
