"""Permissions and Self services."""

from __future__ import annotations

from jumpserver.models.permission import (
    AssetPermAssetRelation,
    AssetPermAssetRelationDetail,
    AssetPermission,
    AssetPermissionRequest,
    AssetPermNodeRelation,
    AssetPermNodeRelationDetail,
    AssetPermUserGroupRelation,
    AssetPermUserGroupRelationDetail,
    AssetPermUserRelation,
    AssetPermUserRelationDetail,
    SelfAsset,
    SelfAssetDetail,
)
from jumpserver.services import BaseService, _from_dict

__all__ = ["PermsService", "SelfService"]


class PermsService(BaseService):
    """CRUD for /api/v1/perms/asset-permissions/."""

    list_url = "/api/v1/perms/asset-permissions/"
    detail_url = "/api/v1/perms/asset-permissions/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(AssetPermission, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(AssetPermission, id)

    def create(self, req: AssetPermissionRequest):
        return self._create(AssetPermission, req)

    def update(self, id: str, req: AssetPermissionRequest):
        return self._update(AssetPermission, id, req)

    def delete(self, id: str):
        return self._delete(id)

    def add_users_relations(self, reqs: list[AssetPermUserRelation]):
        data, resp = self._client.post("/api/v1/perms/asset-permissions-users-relations/", reqs)
        items = [_from_dict(AssetPermUserRelationDetail, item) for item in (data or [])]
        return items, resp

    def add_user_groups_relations(self, reqs: list[AssetPermUserGroupRelation]):
        data, resp = self._client.post(
            "/api/v1/perms/asset-permissions-user-groups-relations/", reqs
        )
        items = [_from_dict(AssetPermUserGroupRelationDetail, item) for item in (data or [])]
        return items, resp

    def add_assets_relations(self, reqs: list[AssetPermAssetRelation]):
        data, resp = self._client.post("/api/v1/perms/asset-permissions-assets-relations/", reqs)
        items = [_from_dict(AssetPermAssetRelationDetail, item) for item in (data or [])]
        return items, resp

    def add_nodes_relations(self, reqs: list[AssetPermNodeRelation]):
        data, resp = self._client.post("/api/v1/perms/asset-permissions-nodes-relations/", reqs)
        items = [_from_dict(AssetPermNodeRelationDetail, item) for item in (data or [])]
        return items, resp

    def get_self_asset_accounts(self, asset_id: str):
        data, resp = self._client.get(f"/api/v1/perms/users/self/assets/{asset_id}/")
        return data or {}, resp


class SelfService(BaseService):
    """Service for /api/v1/perms/users/self/ endpoints."""

    def list_assets(self, filters: dict = None, limit=None, offset=None, search=None):
        params = {}
        if filters:
            params.update(filters)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        data, resp = self._client.get("/api/v1/perms/users/self/assets/", params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(SelfAsset, item) for item in results], resp

    def get_asset(self, asset_id: str):
        data, resp = self._client.get(f"/api/v1/perms/users/self/assets/{asset_id}/")
        return _from_dict(SelfAssetDetail, data) if data else None, resp
