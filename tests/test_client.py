"""Integration tests for the JumpServer Python SDK.

All tests below call real JumpServer APIs via environment variables.

Supported auth methods (checked in order):

1. Access Key (HMAC-SHA256 signature):
       JUMPSERVER_URL          - JumpServer base URL
       JUMPSERVER_KEY_ID       - Access Key ID
       JUMPSERVER_SECRET_ID    - Access Key Secret

2. Username + Password (POST /api/v1/authentication/auth/ → Bearer token):
       JUMPSERVER_URL          - JumpServer base URL
       JUMPSERVER_USERNAME     - Username
       JUMPSERVER_PASSWORD     - Password

Unit tests (TestAuth, TestErrors, TestModels) run unconditionally.
Integration tests are skipped when env vars are not set.
"""

import os

import pytest
import requests

from jumpserver import Client
from jumpserver.auth import (
    BearerTokenAuth,
    PasswordAuth,
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

# ---------------------------------------------------------------------------
# Env-var credentials
# ---------------------------------------------------------------------------

BASE_URL = os.environ.get("JUMPSERVER_URL") or ""
AK = os.environ.get("JUMPSERVER_KEY_ID") or ""
SK = os.environ.get("JUMPSERVER_SECRET_ID") or ""
USERNAME = os.environ.get("JUMPSERVER_USERNAME") or ""
PASSWORD = os.environ.get("JUMPSERVER_PASSWORD") or ""

requires_env = pytest.mark.skipif(
    not (BASE_URL and ((AK and SK) or (USERNAME and PASSWORD))),
    reason=(
        "JUMPSERVER_URL + (KEY_ID/SECRET_ID or USERNAME/PASSWORD) not set"
    ),
)


@pytest.fixture(scope="module")
def client() -> Client:
    """Shared Client authenticated via env vars (AK/SK or username/password)."""
    if AK and SK:
        return Client(base_url=BASE_URL, access_key=AK, access_secret=SK)
    return Client(base_url=BASE_URL, username=USERNAME, password=PASSWORD)


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

    def test_password_auth_sets_bearer_header(self):
        """PasswordAuth fetches a Bearer token via real API."""
        if not (BASE_URL and USERNAME and PASSWORD):
            pytest.skip("JUMPSERVER_USERNAME / JUMPSERVER_PASSWORD not set")
        auth = PasswordAuth(
            base_url=BASE_URL,
            username=USERNAME,
            password=PASSWORD,
        )
        req = requests.Request("GET", f"{BASE_URL}/api/v1/users/profile/")
        prepped = req.prepare()
        auth(prepped)
        assert "Authorization" in prepped.headers
        assert prepped.headers["Authorization"].startswith("Bearer ")

    def test_password_auth_token_cached(self):
        """PasswordAuth caches the token across multiple calls."""
        if not (BASE_URL and USERNAME and PASSWORD):
            pytest.skip("JUMPSERVER_USERNAME / JUMPSERVER_PASSWORD not set")
        auth = PasswordAuth(
            base_url=BASE_URL,
            username=USERNAME,
            password=PASSWORD,
        )
        # First call — fetches token from API
        req1 = requests.Request("GET", f"{BASE_URL}/api/v1/users/profile/")
        prepped1 = req1.prepare()
        auth(prepped1)
        token1 = prepped1.headers["Authorization"]

        # Second call — should reuse cached token (no new API call)
        req2 = requests.Request("GET", f"{BASE_URL}/api/v1/users/profile/")
        prepped2 = req2.prepare()
        auth(prepped2)
        token2 = prepped2.headers["Authorization"]

        assert token1 == token2

    def test_signature_auth_requires_key(self):
        with pytest.raises(ValueError):
            SignatureAuth("", "")

    def test_signature_auth_directly(self):
        """SignatureAuth correctly signs a PreparedRequest."""
        auth = SignatureAuth("my-key", "my-secret")
        req = requests.Request("GET", "http://example.com/api/v1/users/profile/")
        prepped = req.prepare()
        auth(prepped)
        assert "Date" in prepped.headers
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


# ------------------------------------------------------------------
# Unit: Errors
# ------------------------------------------------------------------


class TestErrors:
    def test_api_error_message_from_detail(self):
        err = map_error(404, "GET", "http://example.com/api/", body=b'{"detail":"Not found."}')
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
# Unit: Client construction (no network)
# ------------------------------------------------------------------


class TestClient:
    def test_default_org_header(self):
        """Default org header should be the global org."""
        client = Client(base_url="http://127.0.0.1")
        assert client._session.headers.get("X-JMS-ORG") == "00000000-0000-0000-0000-000000000002"

    def test_services_are_wired(self):
        client = Client(base_url="http://127.0.0.1")
        assert client.users is not None
        assert client.assets is not None
        assert client.accounts is not None
        assert client.organizations is not None
        assert client.hosts is not None
        assert client.databases is not None
        assert client.auth is not None

    def test_with_org_returns_new_client(self):
        client = Client(base_url="http://127.0.0.1")
        org_client = client.with_org("my-org-id")
        assert org_client is not client
        assert org_client._org_id == "my-org-id"


# ------------------------------------------------------------------
# Unit: Model creation (no network)
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
# Integration: Client connectivity
# ------------------------------------------------------------------


@requires_env
class TestIntegrationClient:
    def test_client_has_auth(self, client: Client):
        """Client constructed from env vars should have auth configured."""
        assert client._auth is not None

    def test_get_request(self, client: Client):
        """GET a known endpoint and verify response structure."""
        data, resp = client.get("/api/v1/users/users/", params={"limit": 1})
        assert resp.status_code == 200
        assert "count" in data
        assert "results" in data

    def test_post_returns_error_for_invalid_body(self, client: Client):
        """POST with invalid data should raise APIError."""
        with pytest.raises(APIError):
            client.post("/api/v1/assets/host/", {"name": ""})


# ------------------------------------------------------------------
# Integration: Users service
# ------------------------------------------------------------------


@requires_env
class TestIntegrationUsers:
    def test_profile(self, client: Client):
        user, resp = client.users.profile()
        assert resp.status_code == 200
        assert user is not None
        assert user.username != ""

    def test_list_users(self, client: Client):
        users, resp = client.users.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(users, list)
        if users:
            assert users[0].id != ""

    def test_list_users_with_offset(self, client: Client):
        users, resp = client.users.list(limit=2, offset=0)
        assert resp.status_code == 200
        assert isinstance(users, list)

    def test_list_users_with_search(self, client: Client):
        users, resp = client.users.list(limit=5, search="admin")
        assert resp.status_code == 200
        assert isinstance(users, list)

    def test_user_groups(self, client: Client):
        """List user groups endpoint."""
        groups, resp = client.user_groups.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(groups, list)


# ------------------------------------------------------------------
# Integration: Assets service
# ------------------------------------------------------------------


@requires_env
class TestIntegrationAssets:
    def test_list_assets(self, client: Client):
        assets, resp = client.assets.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(assets, list)

    def test_list_hosts(self, client: Client):
        hosts, resp = client.hosts.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(hosts, list)

    def test_list_databases(self, client: Client):
        databases, resp = client.databases.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(databases, list)

    def test_list_nodes(self, client: Client):
        nodes, resp = client.nodes.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(nodes, list)

    def test_list_platforms(self, client: Client):
        platforms, resp = client.platforms.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(platforms, list)


# ------------------------------------------------------------------
# Integration: Other services
# ------------------------------------------------------------------


@requires_env
class TestIntegrationServices:
    def test_orgs_list(self, client: Client):
        orgs, resp = client.organizations.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(orgs, list)

    def test_settings_public(self, client: Client):
        s, resp = client.settings.public()
        assert resp.status_code == 200
        assert s is not None

    def test_permissions_list(self, client: Client):
        perms, resp = client.permissions.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(perms, list)

    def test_audits_list_sessions(self, client: Client):
        sessions, resp = client.audits.list_sessions(limit=5)
        assert resp.status_code == 200
        assert isinstance(sessions, list)

    def test_labels_list(self, client: Client):
        labels, resp = client.labels.list(limit=5)
        assert resp.status_code == 200
        assert isinstance(labels, list)

    def test_with_org_scoping(self, client: Client):
        """with_org should return a client scoped to the given org."""
        org_client = client.with_org("00000000-0000-0000-0000-000000000002")
        users, resp = org_client.users.list(limit=1)
        assert resp.status_code == 200
