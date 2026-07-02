"""Ops / quick-command job service."""

from typing import Optional

from jumpserver.client import Client, Response
from jumpserver.models.extra import OpsJobRequest, OpsJobResponse, OpsJobResult
from jumpserver.services import BaseService
from jumpserver.utils import format_path

__all__ = ["OpsService"]


class OpsService(BaseService):
    """Service for /api/v1/ops/ endpoints."""

    def run_job(self, req: OpsJobRequest):
        data, resp = self._client.post("/api/v1/ops/quick-commands/", req)
        return _from_dict(OpsJobResponse, data) if data else None, resp

    def get_job_result(self, job_id: str):
        data, resp = self._client.get(
            format_path("/api/v1/ops/quick-commands/%s/", job_id)
        )
        return _from_dict(OpsJobResult, data) if data else None, resp


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
