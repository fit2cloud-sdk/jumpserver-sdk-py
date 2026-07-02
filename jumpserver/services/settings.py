"""Settings service."""

from typing import Optional

from jumpserver.client import Client, Response
from jumpserver.models.extra import PublicSetting
from jumpserver.services import BaseService

__all__ = ["SettingsService"]


class SettingsService(BaseService):
    """Service for /api/v1/settings/ endpoints."""

    def public(self):
        data, resp = self._client.get("/api/v1/settings/public/")
        return _from_dict(PublicSetting, data) if data else None, resp

    def list(self, limit=None, offset=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/settings/setting/", params=params)
        return data or {}, resp


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
