"""Ops / quick-command job service."""

from jumpserver.models.extra import OpsJobRequest, OpsJobResponse, OpsJobResult
from jumpserver.services import BaseService, _from_dict
from jumpserver.utils import format_path

__all__ = ["OpsService"]


class OpsService(BaseService):
    """Service for /api/v1/ops/ endpoints."""

    def run_job(self, req: OpsJobRequest):
        data, resp = self._client.post("/api/v1/ops/jobs/", req)
        return _from_dict(OpsJobResponse, data) if data else None, resp

    def get_job_result(self, job_id: str):
        data, resp = self._client.get(
            format_path("/api/v1/ops/job-execution/task-detail/%s/", job_id)
        )
        return _from_dict(OpsJobResult, data) if data else None, resp
