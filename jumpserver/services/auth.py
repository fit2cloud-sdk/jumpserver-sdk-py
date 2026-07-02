"""Authentication service."""

from jumpserver.models.auth import (
    ConnectionToken,
    ConnectionTokenRequest,
    SSOLoginRequest,
    Token,
    TokenRequest,
)
from jumpserver.services import BaseService, _from_dict
from jumpserver.utils import format_path

__all__ = ["AuthService"]


class AuthService(BaseService):
    """Service for /api/v1/authentication/ endpoints."""

    def create_token(self, req: TokenRequest):
        data, resp = self._client.post("/api/v1/authentication/tokens/", req)
        return _from_dict(Token, data) if data else None, resp

    def confirm_login_status(self, ticket_id: str):
        data, resp = self._client.get(
            f"/api/v1/authentication/login-confirm-ticket/status/?ticket_id={ticket_id}"
        )
        return data or {}, resp

    def select_mfa(self, ticket_id: str, mfa_type: str):
        body = {"mfa_type": mfa_type}
        data, resp = self._client.post(
            f"/api/v1/authentication/mfa/select/?ticket_id={ticket_id}", body
        )
        return data or {}, resp

    def create_connection_token(self, req: ConnectionTokenRequest):
        data, resp = self._client.post("/api/v1/authentication/connection-token/", req)
        return _from_dict(ConnectionToken, data) if data else None, resp

    def create_super_connection_token(self, req: ConnectionTokenRequest):
        data, resp = self._client.post("/api/v1/authentication/super-connection-token/", req)
        return _from_dict(ConnectionToken, data) if data else None, resp

    def get_super_connection_token_secret(self, token_id: str):
        body = {"id": token_id, "expire_now": False}
        data, resp = self._client.post(
            "/api/v1/authentication/super-connection-token/secret/", body
        )
        return data or {}, resp

    def sso_login_url(self, req: SSOLoginRequest):
        data, resp = self._client.post("/api/v1/authentication/sso/login-url/", req)
        return data or {}, resp

    def get_client_url(self, token_id: str):
        data, resp = self._client.get(
            format_path("/api/v1/authentication/connection-token/%s/client-url/", token_id)
        )
        url = (data or {}).get("url", "")
        return url, resp
