"""Audits / sessions / logs service."""
from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO, Optional

from jumpserver.models.audit import Command, FTPLog, LoginLog, OperateLog, Session
from jumpserver.services import BaseService, from_dict
from jumpserver.utils import format_path

if TYPE_CHECKING:
    from jumpserver.client import Response




__all__ = ["AuditsService"]

class AuditsService(BaseService):
    """Service for session, command, and log endpoints."""
    def list_sessions(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[Session], Response]:
        path = "/api/v1/terminal/sessions/"
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        data, resp = self._client.get(path, params=params)
        results = (data or {}).get("results", [])
        return [from_dict(Session, item) for item in results], resp

    def get_session(self, id: str) -> tuple[Optional[Session], Response]:
        path = format_path("/api/v1/terminal/sessions/%s/", id)
        data, resp = self._client.get(path)
        return from_dict(Session, data) if data else None, resp

    def download_replay(self, session_id: str, writer: BinaryIO):
        path = format_path("/api/v1/terminal/sessions/%s/replay/", session_id)
        resp = self._client.stream(path, writer)
        return resp

    def list_commands(self, limit: int = 10, offset: Optional[int] = None, session_id: Optional[str] = None) -> tuple[list[Command], Response]:
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        if session_id:
            params["session"] = session_id
        data, resp = self._client.get("/api/v1/terminal/commands/", params=params)
        results = (data or {}).get("results", [])
        return [from_dict(Command, item) for item in results], resp

    def list_ftp_logs(self, limit: int = 10, offset: Optional[int] = None, session_id: Optional[str] = None) -> tuple[list[FTPLog], Response]:
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        if session_id:
            params["session"] = session_id
        data, resp = self._client.get("/api/v1/audits/ftp-logs/", params=params)
        results = (data or {}).get("results", [])
        return [from_dict(FTPLog, item) for item in results], resp

    def list_login_logs(self, limit: int = 10, offset: Optional[int] = None) -> tuple[list[LoginLog], Response]:
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/audits/login-logs/", params=params)
        results = (data or {}).get("results", [])
        return [from_dict(LoginLog, item) for item in results], resp

    def list_operate_logs(self, limit: int = 10, offset: Optional[int] = None) -> tuple[list[OperateLog], Response]:
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/audits/operate-logs/", params=params)
        results = (data or {}).get("results", [])
        return [from_dict(OperateLog, item) for item in results], resp
