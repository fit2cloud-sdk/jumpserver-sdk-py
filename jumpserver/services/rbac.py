"""RBAC Roles service."""

from jumpserver.models.acl import Role
from jumpserver.services import BaseService, from_dict

__all__ = ["RBACService"]


class RBACService(BaseService):
    """Service for /api/v1/rbac/{scope}-roles/."""

    def list(self, scope: str = "system", limit: int = 10, offset=None, search=None):
        url = f"/api/v1/rbac/{scope}-roles/"
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        data, resp = self._client.get(url, params=params)
        results = (data or {}).get("results", [])
        return [from_dict(Role, item) for item in results], resp

    def get(self, scope: str, id: str):
        url = f"/api/v1/rbac/{scope}-roles/{id}/"
        data, resp = self._client.get(url)
        return from_dict(Role, data) if data else None, resp
