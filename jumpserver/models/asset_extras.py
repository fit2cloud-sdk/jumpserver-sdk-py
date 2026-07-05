from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from . import IDName, LabelValue, NamePort, PlatformMini

__all__ = [
    "Node", "NodeRequest", "NodeChildRequest", "NodeTreeItem",
    "Platform", "PlatformProtocol",
    "Zone", "ZoneRequest",
    "Gateway", "GatewayRequest",
]


@dataclass
class PlatformProtocol:
    """Rich protocol binding returned by the platform API."""

    id: int = 0
    name: str = ""
    port: int = 0
    port_from_addr: bool = False
    primary: bool = False
    required: bool = False
    default: bool = False
    public: bool = True
    secret_types: list[str] = field(default_factory=list)
    setting: dict[str, Any] = field(default_factory=dict)


@dataclass
class Node:
    id: str = ""
    key: str = ""
    value: str = ""
    full_value: str = ""
    org_id: str = ""
    assets_amount: int = 0
    parent: str = ""


@dataclass
class NodeRequest:
    value: str = ""
    parent: str = ""


@dataclass
class NodeChildRequest:
    value: str = ""


@dataclass
class NodeTreeItem:
    id: str = ""
    key: str = ""
    value: str = ""
    org_id: str = ""
    name: str = ""
    full_value: str = ""
    org_name: str = ""


@dataclass
class Platform:
    id: int = 0
    name: str = ""
    category: Optional[LabelValue] = None
    type: Optional[LabelValue] = None
    charset: Optional[LabelValue] = None
    internal: bool = False
    domain_enabled: bool = False
    su_enabled: bool = False
    protocols: list[PlatformProtocol] = field(default_factory=list)
    comment: str = ""
    created_by: str = ""
    updated_by: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class Zone:
    id: str = ""
    name: str = ""
    assets: list[IDName] = field(default_factory=list)
    gateways: list[IDName] = field(default_factory=list)
    assets_amount: int = 0
    labels: list[IDName] = field(default_factory=list)
    comment: str = ""
    org_id: str = ""
    org_name: str = ""
    created_by: str = ""
    updated_by: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class ZoneRequest:
    name: str = ""
    assets: list[str] = field(default_factory=list)
    gateways: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    comment: str = ""


@dataclass
class Gateway:
    id: str = ""
    name: str = ""
    address: str = ""
    platform: Optional[PlatformMini] = None
    protocols: list[PlatformProtocol] = field(default_factory=list)
    nodes: list[IDName] = field(default_factory=list)
    is_active: bool = False
    comment: str = ""
    org_id: str = ""
    org_name: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class GatewayRequest:
    name: str = ""
    address: str = ""
    platform: int = 0
    zone: str = ""
    protocols: list[NamePort] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    is_active: bool = True
    comment: str = ""
