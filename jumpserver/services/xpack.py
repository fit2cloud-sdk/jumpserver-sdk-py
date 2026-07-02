"""XPack (enterprise) service."""

from jumpserver.client import Client, Response
from jumpserver.models.extra import License
from jumpserver.services import BaseService

__all__ = ["XpackService"]


class XpackService(BaseService):
    """Service for /api/v1/xpack/ endpoints (enterprise edition only)."""

    def license(self):
        data, resp = self._client.get("/api/v1/xpack/license/detail")
        return _from_dict(License, data) if data else None, resp


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
