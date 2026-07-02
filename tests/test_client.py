"""Tests for the JumpServer Python SDK."""

import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from jumpserver import Client, Response
from jumpserver.auth import (
    BasicAuth,
    BearerTokenAuth,
    PrivateTokenAuth,
    SignatureAuth,
)
from jumpserver.errors import (
    APIError,
    NotFoundError,
    UnauthorizedError,
    is_not_found,
    map_error,
)
from jumpserver.models.auth import TokenRequest
from jumpserver.models.user import GroupRequest, User, UserRequest


# ------------------------------------------------------------------
# Unit: Auth
# ------------------------------------------------------------------


class TestAuth:
    def test_signature_auth_sets_date_and_authorization(self):
        auth = SignatureAuth("kid", "secret")
        req = requests.Request("GET", "http://example.com/api/v1/users/")
        prepped = req.prepare()
        auth(prepped)
        assert "Date" in prepped.headers
        assert "Authorization" in prepped.headers
        assert "Signature" in prepped.headers["Authorization"]
        assert 'keyId="kid"' in prepped.headers["Authorization"]

    def test_bearer_token_auth(self):
        auth = BearerTokenAuth("mytoken")
        req = requests.Request("GET", "http://example.com/")
        prepped = req.prepare()
        auth(prepped)
        assert prepped.headers["Authorization"] == "Bearer mytoken"

    def test_private_token_auth(self):
        auth = PrivateTokenAuth("myprivtoken")
        req = requests.Request("GET", "http://example.com/")
        prepped = req.prepare()
        auth(prepped)
        assert prepped.headers["Authorization"] == "Token myprivtoken"

    def test_basic_auth(self):
        auth = BasicAuth("admin", "secret123")
        req = requests.Request("GET", "http://example.com/")
        prepped = req.prepare()
        auth(prepped)
        assert "Authorization" in prepped.headers
        assert prepped.headers["Authorization"].startswith("Basic ")

    def test_signature_auth_requires_key(self):
        with pytest.raises(ValueError):
            SignatureAuth("", "")


# ------------------------------------------------------------------
# Unit: Errors
# ------------------------------------------------------------------


class TestErrors:
    def test_api_error_message_from_detail(self):
        err = map_error(
            404, "GET", "http://example.com/api/", body=b'{"detail":"Not found."}'
        )
        assert isinstance(err, NotFoundError)
        assert "Not found." in str(err)

    def test_api_error_message_from_message(self):
        err = map_error(
            400,
            "POST",
            "http://example.com/api/",
            body=b'{"message":"Invalid input"}',
        )
        assert isinstance(err, APIError)
        assert err.status_code == 400

    def test_not_found_helper(self):
        err = NotFoundError(404, "GET", "http://example.com/")
        assert is_not_found(err)
        assert not is_not_found(ValueError())

    def test_status_code_mapping(self):
        err_401 = map_error(401, "GET", "/", body=b'{"detail":"Unauthorized"}')
        assert isinstance(err_401, UnauthorizedError)


# ------------------------------------------------------------------
# Unit: Client
# ------------------------------------------------------------------


class TestClient:
    def test_default_org_header(self):
        """Default org header should be the global org."""
        client = Client(base_url="http://example.com")
        assert client._session.headers.get("X-JMS-ORG") == "00000000-0000-0000-0000-000000000002"

    def test_services_are_wired(self):
        client = Client(base_url="http://example.com")
        assert client.users is not None
        assert client.assets is not None
        assert client.accounts is not None
        assert client.organizations is not None
        assert client.hosts is not None
        assert client.databases is not None
        assert client.auth is not None

    def test_with_org_returns_new_client(self):
        client = Client(base_url="http://example.com")
        org_client = client.with_org("my-org-id")
        assert org_client is not client
        assert org_client._org_id == "my-org-id"

    @patch("jumpserver.client.requests.Session")
    def test_get_request(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":0,"results":[]}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        data, resp = client.get("/api/v1/users/users/")

        assert data == {"count": 0, "results": []}
        assert resp.status_code == 200

    @patch("jumpserver.client.requests.Session")
    def test_post_creates_resource(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"id":"new-id","name":"test"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        data, resp = client.post("/api/v1/assets/host/", {"name": "test"})

        called_kwargs = mock_session.request.call_args[1]
        assert called_kwargs["method"] == "POST"
        sent_body = json.loads(called_kwargs["data"])
        assert sent_body["name"] == "test"

    @patch("jumpserver.client.requests.Session")
    def test_error_raises_exception(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"detail":"Resource not found"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        with pytest.raises(NotFoundError):
            client.get("/api/v1/missing/")


# ------------------------------------------------------------------
# Integration-style: User service with mock HTTP
# ------------------------------------------------------------------


class TestUsersService:
    @patch("jumpserver.client.requests.Session")
    def test_profile(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"id":"u1","name":"Alice","username":"alice","email":"a@b.com"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        user, resp = client.users.profile()

        assert user is not None
        assert user.id == "u1"
        assert user.name == "Alice"
        assert user.username == "alice"

    @patch("jumpserver.client.requests.Session")
    def test_list_users(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":1,"results":[{"id":"u1","name":"Alice"}]}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        users, resp = client.users.list()

        assert len(users) == 1
        assert users[0].id == "u1"

    @patch("jumpserver.client.requests.Session")
    def test_create_user(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"id":"u-new","name":"Bob","username":"bob"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        req = UserRequest(name="Bob", username="bob", email="bob@b.com")
        user, resp = client.users.create(req)

        assert user is not None
        assert user.id == "u-new"
        assert user.name == "Bob"

    @patch("jumpserver.client.requests.Session")
    def test_delete_user(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 204
        mock_resp.headers = {"Content-Type": ""}
        mock_resp.content = b""
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        resp = client.users.delete("u1")
        assert resp.status_code == 204


# ------------------------------------------------------------------
# Integration-style: Asset service
# ------------------------------------------------------------------


class TestAssetsService:
    @patch("jumpserver.client.requests.Session")
    def test_list_assets(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":1,"results":[{"id":"a1","name":"Server01"}]}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        assets, resp = client.assets.list()

        assert len(assets) == 1
        assert assets[0].id == "a1"

    @patch("jumpserver.client.requests.Session")
    def test_category_create(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"id":"db1","name":"db01"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        from jumpserver.models.asset import AssetRequest

        req = AssetRequest(name="db01", address="10.0.0.1", platform=22)
        asset, resp = client.databases.create(req)

        assert asset is not None
        assert asset.id == "db1"

    @patch("jumpserver.client.requests.Session")
    def test_get_asset(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"id":"a1","name":"MyHost","address":"10.0.0.1"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        asset, resp = client.assets.get("a1")

        assert asset is not None
        assert asset.id == "a1"
        assert asset.name == "MyHost"


# ------------------------------------------------------------------
# Integration-style: Other services
# ------------------------------------------------------------------


class TestOtherServices:
    @patch("jumpserver.client.requests.Session")
    def test_auth_create_token(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"token":"v4-token","user":"alice"}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        tok, resp = client.auth.create_token(
            TokenRequest(username="alice", password="secret")
        )

        assert tok is not None
        assert tok.token == "v4-token"

    @patch("jumpserver.client.requests.Session")
    def test_orgs_list(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":1,"results":[{"id":"o1","name":"Default Org"}]}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        orgs, resp = client.organizations.list()
        assert len(orgs) == 1
        assert orgs[0].name == "Default Org"

    @patch("jumpserver.client.requests.Session")
    def test_node_list(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":1,"results":[{"id":"n1","value":"/Root"}]}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        nodes, resp = client.nodes.list()
        assert len(nodes) == 1
        assert nodes[0].id == "n1"

    @patch("jumpserver.client.requests.Session")
    def test_settings_public(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"enable_watermark":false}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        s, resp = client.settings.public()
        assert s is not None

    @patch("jumpserver.client.requests.Session")
    def test_walk_all_pages_mechanism(self, mock_session_cls):
        """Test that ListOptions pagination parameters are sent correctly."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":2,"results":[{"id":"u1"},{"id":"u2"}],"next":null}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        users, resp = client.users.list(limit=10, offset=0)

        assert len(users) == 2
        # Verify limit/offset in request
        called_url = mock_session.request.call_args[1]["url"]
        assert "limit=10" in called_url

    @patch("jumpserver.client.requests.Session")
    def test_permissions_list(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "application/json"}
        mock_resp.content = b'{"count":1,"results":[{"id":"p1","name":"SSH Access"}]}'
        mock_session.request.return_value = mock_resp

        client = Client(base_url="http://example.com")
        perms, resp = client.permissions.list()
        assert len(perms) == 1
        assert perms[0].id == "p1"


# ------------------------------------------------------------------
# Smoke test: Model creation
# ------------------------------------------------------------------


class TestModels:
    def test_user_creation(self):
        u = User(id="u1", name="Alice", username="alice")
        assert u.id == "u1"
        assert str(u.name) == "Alice"

    def test_group_request(self):
        req = GroupRequest(name="Admins")
        assert req.name == "Admins"

    def test_user_request_serialization(self):
        req = UserRequest(
            name="Alice",
            username="alice",
            email="alice@example.com",
            groups=["g1"],
            system_roles=["r1"],
        )
        d = req.__dataclass_fields__
        assert "name" in d
        assert "username" in d

    def test_token_request(self):
        req = TokenRequest(username="admin", password="secret")
        assert req.username == "admin"
        assert req.password == "secret"


# ------------------------------------------------------------------
# Client with AccessKey authentication
# ------------------------------------------------------------------


class TestAccessKeyClient:
    def test_signature_auth_directly(self):
        """Test that SignatureAuth correctly signs a PreparedRequest."""
        import datetime
        from unittest.mock import MagicMock, patch

        auth = SignatureAuth("my-key", "my-secret")
        req = requests.Request("GET", "http://example.com/api/v1/users/profile/")
        prepped = req.prepare()
        auth(prepped)

        # Verify Date was set
        assert "Date" in prepped.headers
        # Verify Authorization was set with Signature
        assert "Authorization" in prepped.headers
        assert "Signature" in prepped.headers["Authorization"]
        assert 'keyId="my-key"' in prepped.headers["Authorization"]

    def test_signature_auth_with_preserved_date(self):
        """When Date is already set, SignatureAuth preserves it."""
        auth = SignatureAuth("my-key", "my-secret")
        req = requests.Request("GET", "http://example.com/api/v1/users/profile/")
        prepped = req.prepare()
        prepped.headers["Date"] = "Sun, 09 Jun 2024 12:00:00 GMT"
        auth(prepped)

        assert prepped.headers["Date"] == "Sun, 09 Jun 2024 12:00:00 GMT"
        assert "Signature" in prepped.headers["Authorization"]
