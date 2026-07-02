"""Settings service."""

from jumpserver.models.extra import PublicSetting
from jumpserver.services import BaseService, _from_dict

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
