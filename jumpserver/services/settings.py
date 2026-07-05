"""Settings service."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from jumpserver.models.extra import PublicSetting
from jumpserver.services import BaseService, from_dict

if TYPE_CHECKING:
    from jumpserver.client import Response



__all__ = ["SettingsService"]

class SettingsService(BaseService):
    """Service for /api/v1/settings/ endpoints."""
    def public(self) -> tuple[Optional[PublicSetting], Response]:
        data, resp = self._client.get("/api/v1/settings/public/")
        return from_dict(PublicSetting, data) if data else None, resp

    def list(self, limit: int = 10, offset: Optional[int] = None) -> tuple[dict, Response]:
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/settings/setting/", params=params)
        return data or {}, resp
