"""Terminal registration & config service."""

from typing import Any

from jumpserver.services import BaseService
from jumpserver.utils import format_path

__all__ = ["TerminalService"]


class TerminalService(BaseService):
    """Service for /api/v1/terminal/ endpoints (Koko, Lion, etc.)."""

    def register(self, name: str, type_name: str, comment: str = ""):
        body = {"name": name, "type": type_name, "comment": comment}
        data, resp = self._client.post("/api/v1/terminal/terminal-registrations/", body)
        return data or {}, resp

    def config(self):
        data, resp = self._client.get("/api/v1/terminal/terminals/config/")
        return data or {}, resp

    def heartbeat(self, statuses: Any):
        _, resp = self._client.post("/api/v1/terminal/terminals/status/", statuses)
        return resp

    def connect_methods(self):
        data, resp = self._client.get("/api/v1/terminal/components/connect-methods/")
        return data or {}, resp

    def get_task(self, task_id: str):
        data, resp = self._client.get(format_path("/api/v1/terminal/tasks/%s/", task_id))
        return data or {}, resp
