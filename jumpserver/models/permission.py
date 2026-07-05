from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from . import IDName, LabelValue, PlatformMini

__all__ = [
    "AssetPermission", "AssetPermissionRequest",
    "AssetPermUserRelation", "AssetPermUserRelationDetail",
    "AssetPermUserGroupRelation", "AssetPermUserGroupRelationDetail",
    "AssetPermAssetRelation", "AssetPermAssetRelationDetail",
    "AssetPermNodeRelation", "AssetPermNodeRelationDetail",
    "SelfAsset", "SelfAssetDetail",
]


@dataclass
class AssetPermission:
    id: str = ""
    name: str = ""
    users: list[IDName] = field(default_factory=list)
    user_groups: list[IDName] = field(default_factory=list)
    assets: list[IDName] = field(default_factory=list)
    nodes: list[IDName] = field(default_factory=list)
    accounts: list[str] = field(default_factory=list)
    protocols: list[str] = field(default_factory=list)
    actions: list[LabelValue] = field(default_factory=list)
    is_active: bool = False
    date_start: str = ""
    date_expired: str = ""
    comment: str = ""
    org_id: str = ""
    org_name: str = ""
    created_by: str = ""
    date_created: str = ""
    date_updated: str = ""


@dataclass
class AssetPermissionRequest:
    name: str = ""
    users: list[str] = field(default_factory=list)
    user_groups: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    nodes: list[str] = field(default_factory=list)
    accounts: list[str] = field(default_factory=list)
    protocols: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    is_active: bool = True
    date_start: str = ""
    date_expired: str = ""
    comment: str = ""


@dataclass
class AssetPermUserRelation:
    user: str = ""
    assetpermission: str = ""


@dataclass
class AssetPermUserRelationDetail:
    id: int = 0
    user: str = ""
    user_display: str = ""
    assetpermission: str = ""
    assetpermission_display: str = ""


@dataclass
class AssetPermUserGroupRelation:
    usergroup: str = ""
    assetpermission: str = ""


@dataclass
class AssetPermUserGroupRelationDetail:
    id: int = 0
    usergroup: str = ""
    usergroup_display: str = ""
    assetpermission: str = ""
    assetpermission_display: str = ""


@dataclass
class AssetPermAssetRelation:
    asset: str = ""
    assetpermission: str = ""


@dataclass
class AssetPermAssetRelationDetail:
    id: int = 0
    asset: str = ""
    asset_display: str = ""
    assetpermission: str = ""
    assetpermission_display: str = ""


@dataclass
class AssetPermNodeRelation:
    node: str = ""
    assetpermission: str = ""


@dataclass
class AssetPermNodeRelationDetail:
    id: int = 0
    node: str = ""
    node_display: str = ""
    assetpermission: str = ""
    assetpermission_display: str = ""


@dataclass
class SelfAsset:
    id: str = ""
    name: str = ""
    address: str = ""
    zone: Any = None
    platform: Optional[PlatformMini] = None
    org_id: str = ""
    connectivity: Optional[LabelValue] = None
    nodes: list[IDName] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    category: Optional[LabelValue] = None
    type: Optional[LabelValue] = None
    org_name: str = ""
    is_active: bool = False
    date_verified: str = ""
    date_created: str = ""
    comment: str = ""
    created_by: str = ""


@dataclass
class PermedProtocolSetting:
    console: Any = None
    security: str = ""
    sftp_home: str = ""
    sftp_enabled: bool = False


@dataclass
class PermedProtocol:
    name: str = ""
    port: int = 0
    public: bool = False
    setting: Optional[PermedProtocolSetting] = None


@dataclass
class PermedAccount:
    id: str = ""
    alias: str = ""
    name: str = ""
    username: str = ""
    has_username: bool = False
    has_secret: bool = False
    secret_type: str = ""
    actions: list[LabelValue] = field(default_factory=list)
    date_expired: str = ""


@dataclass
class SelfAssetDetail:
    id: str = ""
    name: str = ""
    address: str = ""
    zone: Any = None
    platform: Optional[PlatformMini] = None
    org_id: str = ""
    connectivity: Optional[LabelValue] = None
    nodes: list[IDName] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    category: Optional[LabelValue] = None
    type: Optional[LabelValue] = None
    org_name: str = ""
    is_active: bool = False
    date_verified: str = ""
    date_created: str = ""
    comment: str = ""
    created_by: str = ""
    spec_info: Any = None
    permed_protocols: list[PermedProtocol] = field(default_factory=list)
    permed_accounts: list[PermedAccount] = field(default_factory=list)
