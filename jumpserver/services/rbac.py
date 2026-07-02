"""RBAC Roles service."""

from jumpserver.models.acl import Role
from jumpserver.services import BaseService, _from_dict

__all__ = ["RBACService"]


class RBACService(BaseService):
    """Service for /api/v1/rbac/{scope}-roles/."""

    def list(self, scope: str = "system", limit=None, offset=None, search=None):
        url = f"/api/v1/rbac/{scope}-roles/"
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        data, resp = self._client.get(url, params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(Role, item) for item in results], resp

    def get(self, scope: str, id: str):
        url = f"/api/v1/rbac/{scope}-roles/{id}/"
        data, resp = self._client.get(url)
        return _from_dict(Role, data) if data else None, resp
