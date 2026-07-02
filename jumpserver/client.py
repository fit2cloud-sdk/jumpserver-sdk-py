"""JumpServer SDK - Core Client.

The :class:`Client` is the main entry point. Construct one with :func:`Client`
and use its service attributes to make API calls.
"""

from __future__ import annotations

import copy
import json
import logging
import time
from typing import Any, BinaryIO, Callable, Optional, TypeVar
from urllib.parse import urljoin

import requests

from . import auth as authmod
from .errors import map_error

T = TypeVar("T")

# Default organization ID (global org)
JMS_GLOBAL_ORG = "00000000-0000-0000-0000-000000000002"
ORG_HEADER_KEY = "X-JMS-ORG"

_LOGGER = logging.getLogger("jumpserver")

__all__ = [
    "Client",
    "Response",
]


class Response:
    """Wraps a ``requests.Response`` with pagination metadata."""

    def __init__(self, resp: requests.Response) -> None:
        self._resp = resp
        self.count: int = 0
        self.next: Optional[str] = None
        self.previous: Optional[str] = None

    @property
    def status_code(self) -> int:
        return self._resp.status_code

    @property
    def headers(self) -> requests.structures.CaseInsensitiveDict:
        return self._resp.headers

    def has_next(self) -> bool:
        return bool(self.next)

    def has_previous(self) -> bool:
        return bool(self.previous)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._resp, name)


class Client:
    """JumpServer API client.

    Args:
        base_url: JumpServer base URL, e.g. ``https://jumpserver.example.com``.
        access_key: Access Key ID for HMAC-SHA256 auth.
        access_secret: Access Key Secret for HMAC-SHA256 auth.
        username: Username for password-based auth.
        password: Password for password-based auth.
        token: Private token or Bearer token.
        org_id: Default organization ID (default: global org).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Max retries on transient errors (default: 3).
        user_agent: Custom User-Agent string.
        verify_ssl: Whether to verify TLS certificates (default: True).
        debug: Enable debug request logging.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8080",
        access_key: Optional[str] = None,
        access_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        org_id: str = JMS_GLOBAL_ORG,
        timeout: int = 30,
        max_retries: int = 3,
        user_agent: Optional[str] = None,
        verify_ssl: bool = True,
        debug: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                ORG_HEADER_KEY: org_id,
            }
        )
        self._session.verify = verify_ssl

        self._auth: Optional[authmod.Authenticator] = self._build_auth(
            access_key, access_secret, username, password, token
        )
        self._timeout = timeout
        self._max_retries = max_retries
        self._user_agent = user_agent or "jumpserver-sdk-py/0.1.0"
        self._debug = debug
        self._org_id = org_id

        if user_agent:
            self._session.headers["User-Agent"] = user_agent
        else:
            self._session.headers["User-Agent"] = self._user_agent

        # Wire up services
        self._init_services()

    def _build_auth(
        self,
        access_key: Optional[str] = None,
        access_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Optional[authmod.Authenticator]:
        if access_key and access_secret:
            return authmod.SignatureAuth(access_key, access_secret)
        if username and password:
            return authmod.PasswordAuth(
                base_url=self.base_url,
                username=username,
                password=password,
                verify_ssl=self._session.verify,
            )
        if token:
            return authmod.PrivateTokenAuth(token)
        return None

    def _init_services(self) -> None:
        """Lazy-import and wire all service objects."""
        from .services.accounts import (
            AccountsService,
            BackupService,
            ChangeSecretService,
            TemplatesService,
        )
        from .services.acls import CommandFiltersService, LoginACLsService
        from .services.assets import (
            AssetsService,
            CategoryService,
            GatewaysService,
            NodesService,
            PlatformsService,
            ZonesService,
        )
        from .services.audits import AuditsService
        from .services.auth import AuthService
        from .services.labels import LabelsService
        from .services.ops import OpsService
        from .services.orgs import OrgsService
        from .services.perms import PermsService, SelfService
        from .services.rbac import RBACService
        from .services.settings import SettingsService
        from .services.terminal import TerminalService
        from .services.tickets import TicketsService
        from .services.users import GroupsService, UsersService
        from .services.xpack import XpackService

        self.auth = AuthService(self)
        self.users = UsersService(self)
        self.user_groups = GroupsService(self)
        self.roles = RBACService(self)
        self.assets = AssetsService(self)
        self.hosts = CategoryService(self, "hosts")
        self.devices = CategoryService(self, "devices")
        self.databases = CategoryService(self, "databases")
        self.webs = CategoryService(self, "webs")
        self.clouds = CategoryService(self, "clouds")
        self.customs = CategoryService(self, "customs")
        self.nodes = NodesService(self)
        self.platforms = PlatformsService(self)
        self.zones = ZonesService(self)
        self.gateways = GatewaysService(self)
        self.labels = LabelsService(self)
        self.accounts = AccountsService(self)
        self.account_templates = TemplatesService(self)
        self.change_secrets = ChangeSecretService(self)
        self.account_backups = BackupService(self)
        self.organizations = OrgsService(self)
        self.permissions = PermsService(self)
        self.self_service = SelfService(self)
        self.command_filters = CommandFiltersService(self)
        self.login_acls = LoginACLsService(self)
        self.audits = AuditsService(self)
        self.terminal = TerminalService(self)
        self.tickets = TicketsService(self)
        self.settings = SettingsService(self)
        self.ops = OpsService(self)
        self.xpack = XpackService(self)

    # ------------------------------------------------------------------
    # Request / response
    # ------------------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        body: Any = None,
        raw: bool = False,
        stream: bool = False,
    ) -> tuple[Any, Response]:
        """Execute an HTTP request and return ``(decoded_body, response)``."""
        url = urljoin(self.base_url, path.lstrip("/"))
        req_kwargs: dict[str, Any] = {
            "method": method.upper(),
            "url": url,
        }
        send_kwargs: dict[str, Any] = {
            "timeout": self._timeout,
        }

        if stream:
            send_kwargs["stream"] = True
        if body is not None and not raw:
            req_kwargs["data"] = json.dumps(_to_dict(body), default=str)
        elif body is not None and raw:
            req_kwargs["data"] = body

        # Apply auth
        if self._auth:
            req = requests.Request(**req_kwargs)
            prepped = self._session.prepare_request(req)
            self._auth(prepped)
            # Send the prepared request
            return self._send_prepared(prepped, method, path, send_kwargs)
        else:
            req_kwargs.update(send_kwargs)
            return self._send(req_kwargs, method, path)

    def _send(self, kwargs: dict, method: str, path: str) -> tuple[Any, Response]:
        resp = self._do_with_retry(lambda: self._session.request(**kwargs))
        return self._handle_response(resp, method, path)

    def _send_prepared(
        self, prepped: requests.PreparedRequest, method: str, path: str, send_kwargs: dict
    ) -> tuple[Any, Response]:
        resp = self._do_with_retry(lambda: self._session.send(prepped, **send_kwargs))
        return self._handle_response(resp, method, path)

    def _do_with_retry(self, do_call: Callable[[], requests.Response]) -> requests.Response:
        """Execute *do_call* with exponential backoff retry."""
        last_exc: Optional[Exception] = None
        reauth_done = False
        for attempt in range(self._max_retries + 1):
            try:
                resp = do_call()
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exc = exc
                if attempt < self._max_retries and self._is_transient(exc):
                    _LOGGER.debug("Retry %d after error: %s", attempt + 1, exc)
                    self._sleep(attempt, None)
                    continue
                raise

            # 401 auto-refresh: when using PasswordAuth, invalidate the
            # cached token and retry once without counting it as a retry.
            if resp.status_code == 401 and not reauth_done:
                if isinstance(self._auth, authmod.PasswordAuth):
                    _LOGGER.debug("Got 401, invalidating PasswordAuth token")
                    self._auth.invalidate()
                    reauth_done = True
                    continue

            if not self._is_retryable(resp.status_code):
                return resp

            if attempt < self._max_retries:
                _LOGGER.debug("Retry %d after HTTP %d", attempt + 1, resp.status_code)
                self._sleep(attempt, resp)
                continue
            return resp

        raise last_exc or RuntimeError("unreachable")

    def _is_transient(self, exc: Exception) -> bool:
        msg = str(exc).lower()
        if isinstance(exc, requests.Timeout):
            return True
        for kw in ("connection reset", "broken pipe", "connection refused"):
            if kw in msg:
                return True
        return "temporary failure" in msg

    def _is_retryable(self, status: int) -> bool:
        return status in (408, 429, 500, 502, 503, 504)

    def _sleep(self, attempt: int, resp: Optional[requests.Response]) -> None:
        import random

        if resp is not None and "Retry-After" in resp.headers:
            try:
                wait = int(resp.headers["Retry-After"])
                time.sleep(min(wait, 15))
                return
            except ValueError:
                pass
        wait = min(0.5 * (2**attempt), 15)
        jitter = random.uniform(wait / 2, wait)
        time.sleep(jitter)

    def _handle_response(
        self, resp: requests.Response, method: str, path: str
    ) -> tuple[Any, Response]:
        """Decode *resp* and return ``(data, wrapped_response)``."""
        if self._debug:
            _LOGGER.debug("%s %s -> %s", method, path, resp.status_code)

        wrapped = Response(resp)

        # Try to decode JSON body
        body_bytes = resp.content
        content_type = resp.headers.get("Content-Type", "")

        if body_bytes and "json" in content_type:
            try:
                data = json.loads(body_bytes)
            except json.JSONDecodeError:
                data = None
            # Parse pagination
            if isinstance(data, dict):
                wrapped.count = data.get("count", 0) or 0
                wrapped.next = data.get("next") or None
                wrapped.previous = data.get("previous") or None
        else:
            data = body_bytes if body_bytes else None

        if resp.status_code >= 400:
            raise map_error(
                resp.status_code,
                method,
                resp.url,
                body=body_bytes,
            )

        return data, wrapped

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def with_org(self, org_id: str) -> Client:
        """Return a new :class:`Client` scoped to *org_id*."""
        new_client = copy.copy(self)
        new_client._org_id = org_id
        new_client._session = requests.Session()
        new_client._session.headers.update(self._session.headers)
        new_client._session.headers[ORG_HEADER_KEY] = org_id
        new_client._session.verify = self._session.verify
        new_client._auth = self._auth
        new_client._init_services()
        return new_client

    def get(self, path: str, params: Optional[dict] = None) -> tuple[Any, Response]:
        """Perform a GET request."""
        return self._request("GET", _append_query(path, params))

    def post(self, path: str, body: Any = None) -> tuple[Any, Response]:
        """Perform a POST request."""
        return self._request("POST", path, body)

    def patch(self, path: str, body: Any = None) -> tuple[Any, Response]:
        """Perform a PATCH request."""
        return self._request("PATCH", path, body)

    def put(self, path: str, body: Any = None) -> tuple[Any, Response]:
        """Perform a PUT request."""
        return self._request("PUT", path, body)

    def delete(self, path: str) -> tuple[Any, Response]:
        """Perform a DELETE request."""
        return self._request("DELETE", path)

    def stream(self, path: str, writer: BinaryIO) -> Response:
        """Stream a binary response (e.g. session replay) into *writer*."""
        url = urljoin(self.base_url, path.lstrip("/"))
        kwargs: dict[str, Any] = {
            "method": "GET",
            "url": url,
            "timeout": self._timeout,
            "stream": True,
        }
        if self._auth:
            req = requests.Request(**kwargs)
            prepped = self._session.prepare_request(req)
            self._auth(prepped)
            resp = self._session.send(prepped, stream=True, timeout=self._timeout)
        else:
            resp = self._session.request(**kwargs)
        if resp.status_code >= 400:
            raise map_error(resp.status_code, "GET", resp.url, body=resp.content)
        for chunk in resp.iter_content(chunk_size=65536):
            writer.write(chunk)
        return Response(resp)


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _append_query(path: str, params: Optional[dict]) -> str:
    if not params:
        return path
    filtered = {k: v for k, v in params.items() if v is not None and v != ""}
    if not filtered:
        return path
    from urllib.parse import urlencode

    qs = urlencode(filtered, doseq=True)
    if "?" in path:
        return f"{path}&{qs}"
    return f"{path}?{qs}"


def _to_dict(obj: Any) -> Any:
    """Convert a dataclass (or list/ dict of dataclasses) to a plain dict with camelCase keys."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_dict(v) for v in obj]
    if hasattr(obj, "__dataclass_fields__"):
        result = {}
        for field_name in obj.__dataclass_fields__:
            val = getattr(obj, field_name)
            # Skip empty / default values for cleaner payloads
            if val is None:
                continue
            if isinstance(val, (list, tuple)) and len(val) == 0:
                continue
            if isinstance(val, str) and val == "":
                continue
            if isinstance(val, bool) and val is False:
                # Keep False for is_active etc.
                pass
            key = _snake_to_camel(field_name)
            result[key] = _to_dict(val)
        return result
    return obj


def _snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase (e.g. org_id -> orgId)."""
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])
