"""JumpServer SDK - Common model types and helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TypeVar

T = TypeVar("T")


@dataclass
class Pagination:
    """Pagination metadata returned by list endpoints."""

    count: int = 0
    next: Optional[str] = None
    previous: Optional[str] = None

    def has_next(self) -> bool:
        return bool(self.next)

    def has_previous(self) -> bool:
        return bool(self.previous)


@dataclass
class IDName:
    """Compact (id, name) reference used throughout JumpServer."""

    id: str
    name: str


@dataclass
class IDDisplay:
    """(id, name, display_name) reference."""

    id: str
    name: str
    display_name: str


@dataclass
class LabelValue:
    """(label, value) pair for enumerated fields."""

    label: str
    value: str


@dataclass
class NamePort:
    """Protocol binding (name + port)."""

    name: str
    port: int


@dataclass
class PlatformMini:
    """Minimal platform reference."""

    id: int
    name: str
    type: str = ""


# Well-known organization IDs
JMS_DEFAULT_ORG = "ROOT"
JMS_GLOBAL_ORG = "00000000-0000-0000-0000-000000000002"

# Asset categories
ASSET_CATEGORY_HOST = "host"
ASSET_CATEGORY_DEVICE = "device"
ASSET_CATEGORY_DATABASE = "database"
ASSET_CATEGORY_WEB = "web"
ASSET_CATEGORY_CLOUD = "cloud"
ASSET_CATEGORY_CUSTOM = "custom"
