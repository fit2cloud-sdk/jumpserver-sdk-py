"""RBAC Roles service."""

from jumpserver.client import Client, Response
from jumpserver.models.acl import Role
from jumpserver.services import BaseService

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


def _from_dict(cls, data):
    import dataclasses

    if not dataclasses.is_dataclass(cls):
        return data
    field_names = {f.name for f in dataclasses.fields(cls)}
    kwargs = {}
    for key, value in data.items():
        snake = key.replace(" ", "_").replace("-", "_")
        if snake in field_names:
            kwargs[snake] = value
        elif key in field_names:
            kwargs[key] = value
    return cls(**kwargs)
