"""XPack (enterprise) service."""

from jumpserver.models.extra import License
from jumpserver.services import BaseService, from_dict

__all__ = ["XpackService"]


class XpackService(BaseService):
    """Service for /api/v1/xpack/ endpoints (enterprise edition only)."""

    def license(self):
        data, resp = self._client.get("/api/v1/xpack/license/detail")
        return from_dict(License, data) if data else None, resp
