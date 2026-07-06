"""Assets, Nodes, Platforms, Zones, Gateways services."""

from __future__ import annotations

from typing import Any, Optional

from jumpserver.client import Client, Response
from jumpserver.models.asset import Asset, AssetRequest
from jumpserver.models.asset_extras import (
    Gateway,
    GatewayRequest,
    Node,
    NodeRequest,
    NodeTreeItem,
    Platform,
    Zone,
    ZoneRequest,
)
from jumpserver.models.user import User
from jumpserver.services import BaseService, from_dict
from jumpserver.utils import format_path

__all__ = [
    "AssetsService",
    "CategoryService",
    "NodesService",
    "PlatformsService",
    "ZonesService",
    "GatewaysService",
]


class AssetsService(BaseService):
    """CRUD for /api/v1/assets/assets/."""

    list_url = "/api/v1/assets/assets/"
    detail_url = "/api/v1/assets/assets/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Asset], Response]:
        return self._list(Asset, filters, limit, offset, search)

    def get(self, id: str) -> tuple[Optional[Asset], Response]:
        return self._get(Asset, id)

    def delete(self, id: str) -> Response:
        return self._delete(id)

    def perm_users(
        self, asset_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> tuple[list[User], Response]:
        path = format_path("/api/v1/assets/assets/%s/perm-users/", asset_id)
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get(path, params=params)
        items = [from_dict(User, item) for item in (data or [])]
        return items, resp


class CategoryService(BaseService):
    """CRUD for a specific asset category (/api/v1/assets/<category>/)."""

    def __init__(self, client: Client, category: str) -> None:
        super().__init__(client)
        self._category = category
        self.list_url = f"/api/v1/assets/{category}/"
        self.detail_url = f"/api/v1/assets/{category}/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Asset], Response]:
        return self._list(Asset, filters, limit, offset, search)

    def get(self, id: str) -> tuple[Optional[Asset], Response]:
        return self._get(Asset, id)

    def create(self, req: AssetRequest) -> tuple[Optional[Asset], Response]:
        return self._create(Asset, req)

    def update(self, id: str, req: AssetRequest) -> tuple[Optional[Asset], Response]:
        return self._update(Asset, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)


class NodesService(BaseService):
    """CRUD for /api/v1/assets/nodes/."""

    list_url = "/api/v1/assets/nodes/"
    detail_url = "/api/v1/assets/nodes/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Node], Response]:
        return self._list(Node, filters, limit, offset, search)

    def get(self, id: str) -> tuple[Optional[Node], Response]:
        return self._get(Node, id)

    def get_children(
        self, parent_id: str
    ) -> tuple[list[NodeTreeItem], Response]:
        path = format_path("/api/v1/assets/nodes/%s/children/", parent_id)
        data, resp = self._client.get(path)
        items = [
            from_dict(NodeTreeItem, item)
            for item in (
                (data or {}).get("results", []) if isinstance(data, dict) else (data or [])
            )
        ]
        return items, resp

    def children_tree(
        self, key: Optional[str] = None
    ) -> tuple[list[NodeTreeItem], Response]:
        """Fetch the node tree, optionally scoped to a node *key*.

        ``GET /api/v1/assets/nodes/children/tree/``
        """
        params: dict[str, Any] = {}
        if key is not None:
            params["key"] = key
        data, resp = self._client.get("/api/v1/assets/nodes/children/tree/", params=params)
        results = (
            (data or {}).get("results", []) if isinstance(data, dict) else (data or [])
        )
        items = [from_dict(NodeTreeItem, item) for item in results]
        return items, resp

    def create_child(self, parent_id: str, value: str) -> tuple[Optional[Node], Response]:
        path = format_path("/api/v1/assets/nodes/%s/children/", parent_id)
        data, resp = self._client.post(path, {"value": value})
        return from_dict(Node, data) if data else None, resp

    def create(self, req: NodeRequest) -> tuple[Optional[Node], Response]:
        return self._create(Node, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)


class PlatformsService(BaseService):
    """Read-only for /api/v1/assets/platforms/."""

    list_url = "/api/v1/assets/platforms/"
    detail_url = "/api/v1/assets/platforms/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Platform], Response]:
        return self._list(Platform, filters, limit, offset, search)

    def get(self, id: int) -> tuple[Optional[Platform], Response]:
        return self._get(Platform, str(id))


class ZonesService(BaseService):
    """CRUD for /api/v1/assets/zones/."""

    list_url = "/api/v1/assets/zones/"
    detail_url = "/api/v1/assets/zones/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Zone], Response]:
        return self._list(Zone, filters, limit, offset, search)

    def get(self, id: str) -> tuple[Optional[Zone], Response]:
        return self._get(Zone, id)

    def create(self, req: ZoneRequest) -> tuple[Optional[Zone], Response]:
        return self._create(Zone, req)

    def update(self, id: str, req: ZoneRequest) -> tuple[Optional[Zone], Response]:
        return self._update(Zone, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)


class GatewaysService(BaseService):
    """CRUD for /api/v1/assets/gateways/."""

    list_url = "/api/v1/assets/gateways/"
    detail_url = "/api/v1/assets/gateways/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Gateway], Response]:
        return self._list(Gateway, filters, limit, offset, search)

    def get(self, id: str) -> tuple[Optional[Gateway], Response]:
        return self._get(Gateway, id)

    def create(self, req: GatewayRequest) -> tuple[Optional[Gateway], Response]:
        return self._create(Gateway, req)

    def update(self, id: str, req: GatewayRequest) -> tuple[Optional[Gateway], Response]:
        return self._update(Gateway, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)
