"""Audits / sessions / logs service."""

from typing import BinaryIO, Optional

from jumpserver.client import Client, Response
from jumpserver.models.audit import Command, FTPLog, LoginLog, OperateLog, Session
from jumpserver.services import BaseService
from jumpserver.utils import format_path

__all__ = ["AuditsService"]


class AuditsService(BaseService):
    """Service for session, command, and log endpoints."""

    def list_sessions(self, limit=None, offset=None, search=None):
        path = "/api/v1/terminal/sessions/"
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        data, resp = self._client.get(path, params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(Session, item) for item in results], resp

    def get_session(self, id: str):
        path = format_path("/api/v1/terminal/sessions/%s/", id)
        data, resp = self._client.get(path)
        return _from_dict(Session, data) if data else None, resp

    def download_replay(self, session_id: str, writer: BinaryIO):
        path = format_path("/api/v1/terminal/sessions/%s/replay/", session_id)
        resp = self._client.stream(path, writer)
        return resp

    def list_commands(self, limit=None, offset=None, session_id=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if session_id:
            params["session"] = session_id
        data, resp = self._client.get("/api/v1/terminal/commands/", params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(Command, item) for item in results], resp

    def list_ftp_logs(self, limit=None, offset=None, session_id=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if session_id:
            params["session"] = session_id
        data, resp = self._client.get("/api/v1/audits/ftp-logs/", params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(FTPLog, item) for item in results], resp

    def list_login_logs(self, limit=None, offset=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/audits/login-logs/", params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(LoginLog, item) for item in results], resp

    def list_operate_logs(self, limit=None, offset=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/audits/operate-logs/", params=params)
        results = (data or {}).get("results", [])
        return [_from_dict(OperateLog, item) for item in results], resp


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
