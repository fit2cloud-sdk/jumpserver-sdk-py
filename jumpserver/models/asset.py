from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from . import IDName, LabelValue, NamePort, PlatformMini

__all__ = [
    "AssetWebScript", "AssetSpecInfo",
    "Asset", "AssetRequest",
]


@dataclass
class AssetWebScript:
    name: str = ""
    type: str = ""
    script: Any = None


@dataclass
class AssetSpecInfo:
    db_name: str = ""
    use_ssl: bool = False
    allow_invalid_cert: bool = False
    autofill: str = ""
    script: list[AssetWebScript] = field(default_factory=list)
    submit_selector: str = ""


@dataclass
class Asset:
    id: str = ""
    name: str = ""
    address: str = ""
    comment: str = ""
    zone: Any = None
    platform: Optional[PlatformMini] = None
    nodes: list[IDName] = field(default_factory=list)
    labels: list[Any] = field(default_factory=list)
    protocols: list[Any] = field(default_factory=list)
    nodes_display: list[str] = field(default_factory=list)
    category: Optional[LabelValue] = None
    type: Optional[LabelValue] = None
    connectivity: Any = None
    created_by: str = ""
    org_id: str = ""
    org_name: str = ""
    is_active: bool = False
    date_verified: Any = None
    date_created: str = ""
    date_updated: str = ""
    spec_info: Any = None
    accounts_amount: int = 0


@dataclass
class AssetRequest:
    name: str = ""
    address: str = ""
    platform: int = 0
    protocols: list[NamePort] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    accounts: list[dict] = field(default_factory=list)
    zone: str = ""
    is_active: bool = True
    comment: str = ""
    spec_info: Optional[AssetSpecInfo] = None
    directory_services: list[str] = field(default_factory=list)
