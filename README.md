[![EN](https://img.shields.io/badge/EN-English-blue)](README.md)
[![CN](https://img.shields.io/badge/CN-中文-red)](README_CN.md)

# jumpserver-sdk-py

Python SDK for the [JumpServer](https://www.jumpserver.org/) REST API, compatible with **v4.10.x**.

[English](README.md) | [中文文档](README_CN.md)

## Features

- **v4 Support** — Targets JumpServer v4.x
- **26+ Service Modules** — Full CRUD: Users, Assets, Accounts, Permissions, Organizations, Tickets, Self-service, Ops, and more
- **Categorized Assets** — Hosts, Network Devices, Databases, Web, Cloud, Custom
- **Multiple Auth Methods** — AccessKey (HMAC-SHA256), Password (Bearer Token), Private Token
- **Password Auth with Token Caching** — Exchanges username/password for a Bearer Token on first request, caches it, and auto-refreshes 5 minutes before expiry; auto-retries on 401
- **Organization Scoping** — `with_org(id)` switches organization context
- **Pagination** — `limit` / `offset` pagination parameters
- **Smart Retry** — Exponential backoff with jitter, retries only transient errors (408/429/5xx)
- **Type Safety** — Full dataclass models with IDE autocompletion

## Requirements

- Python 3.9+

## Installation

```bash
pip install jumpserver-sdk
```

## Quick Start

```python
from jumpserver import Client

# Using AccessKey (recommended for service accounts)
client = Client(
    base_url="https://jumpserver.example.com",
    access_key="your-access-key-id",
    access_secret="your-access-key-secret",
)

# Using username/password (auto-exchanges for Bearer Token with caching)
client = Client(
    base_url="https://jumpserver.example.com",
    username="admin",
    password="password",
)

# Using Private Token
client = Client(
    base_url="https://jumpserver.example.com",
    token="your-private-token",
)

# Get current user profile
user, resp = client.users.profile()
print(user.name, user.username)

# List users
users, resp = client.users.list(limit=20)
for u in users:
    print(u.username, u.email)

# Create a host asset
from jumpserver.models.asset import AssetRequest

asset, resp = client.hosts.create(AssetRequest(
    name="web-01",
    address="192.168.1.10",
    platform=1,
))
print("Created:", asset.id)

# Switch organization scope
org_client = client.with_org("org-id-here")
org_client.assets.list()
```

## Authentication

```python
# AccessKey HMAC-SHA256 (recommended for service accounts)
client = Client(
    base_url="https://jumpserver.example.com",
    access_key="key-id",
    access_secret="secret-id",
)

# Username/password authentication
# First request auto-POSTs to /api/v1/authentication/auth/ to get a Bearer Token
# Token is cached, auto-refreshed 5 minutes before expiry, re-fetched on 401
client = Client(
    base_url="https://jumpserver.example.com",
    username="admin",
    password="password",
)

# Private Token (static)
client = Client(
    base_url="https://jumpserver.example.com",
    token="your-private-token",
)
```

### Password Auth Flow

```
First request  → POST /api/v1/authentication/auth/ {"username": "...", "password": "..."}
               ← Returns {"token": "...", "date_expired": "2026/07/03 11:48:25 +0800"}
               → Caches token and expiry time
               → Sets Authorization: Bearer <token>

Subsequent     → Checks cache:
requests           token exists AND time-to-expiry > 5 min → reuse cache
                   otherwise → re-fetch token

401 received   → Clears cache → re-fetches token → retries once
```

## Error Handling

```python
from jumpserver.errors import APIError, NotFoundError, is_not_found

try:
    user, resp = client.users.get("non-existent-id")
except NotFoundError as e:
    print("Not found (404):", e)
except APIError as e:
    print(f"API error {e.status_code}: {e}")
```

## Services

| Service | Client Field | Methods | Description |
|---------|-------------|---------|-------------|
| Users | `client.users` | list / get / profile / create / update / replace / delete / invite | User CRUD + profile |
| User Groups | `client.user_groups` | list / get / create / update / delete | User group CRUD |
| Roles | `client.roles` | list(scope) / get(scope) | Org/system role query |
| Assets | `client.assets` | list / get / delete / perm_users | Generic asset operations |
| Hosts | `client.hosts` | list / get / create / update / delete | Host CRUD |
| Network Devices | `client.devices` | list / get / create / update / delete | Network device CRUD |
| Databases | `client.databases` | list / get / create / update / delete | Database CRUD |
| Web | `client.webs` | list / get / create / update / delete | Web asset CRUD |
| Cloud | `client.clouds` | list / get / create / update / delete | Cloud asset CRUD |
| Custom | `client.customs` | list / get / create / update / delete | Custom asset CRUD |
| Nodes | `client.nodes` | list / get / create / delete / create_child / get_children | Asset tree node CRUD + children |
| Platforms | `client.platforms` | list / get | Platform template query |
| Zones | `client.zones` | list / get / create / update / delete | Zone CRUD |
| Gateways | `client.gateways` | list / get / create / update / delete | Gateway CRUD |
| Labels | `client.labels` | list / get / create / update / delete | Label CRUD |
| Accounts | `client.accounts` | list / get / create / update / delete / get_secret / create_bulk / verify | Account CRUD + secret view + bulk create |
| Account Templates | `client.account_templates` | list / get / create / update / delete | Template CRUD |
| Change Secret | `client.change_secrets` | list / get / create / update / delete | Change-secret automation CRUD |
| Account Backups | `client.account_backups` | list / get / create / update / delete | Backup plan CRUD |
| Organizations | `client.organizations` | list / get / create / update / delete | Organization CRUD |
| Permissions | `client.permissions` | list / get / create / update / delete / add_users_relations / add_user_groups_relations / add_assets_relations / add_nodes_relations / get_self_asset_accounts | Asset permission CRUD + relations + self-service account query |
| Command Filters | `client.command_filters` | list / get / create / update / delete / list_groups / get_group / create_group / update_group / delete_group | Command filter + command group CRUD |
| Login ACLs | `client.login_acls` | list / get / delete | Login ACL query |
| Audits | `client.audits` | list_sessions / list_commands / list_ftp_logs / list_login_logs / list_operate_logs / get_session / download_replay | Sessions, commands, FTP, login, operate logs |
| Auth | `client.auth` | create_token / create_connection_token / create_super_connection_token / sso_login_url | Login, tokens, SSO |
| Terminal | `client.terminal` | register / config / heartbeat / connect_methods / get_task | Terminal registration, config, heartbeat |
| Tickets | `client.tickets` | list / get / create / approve / reject / list_flows / update_flow | Ticket CRUD + approval + workflow |
| Settings | `client.settings` | public / list | System settings query |
| Self Service | `client.self_service` | list_assets / get_asset | Self-service authorized assets |
| Ops | `client.ops` | run_job / get_job_result | Ops job execution (/api/v1/ops/jobs/) |
| Xpack | `client.xpack` | license | License info |

## Package Structure

```
jumpserver/
├── models/                   # Response & request models (dataclass)
│   ├── user.py               #   User, UserRequest, Group, GroupRequest
│   ├── asset.py              #   Asset, AssetRequest
│   ├── asset_extras.py       #   Node, Platform, Zone, Gateway
│   ├── account.py            #   Account, AccountTemplate, ChangeSecret
│   ├── permission.py         #   AssetPermission, SelfAsset
│   ├── org.py                #   Organization
│   ├── auth.py               #   Token, TokenRequest, ConnectionToken
│   ├── ticket.py             #   Ticket, TicketFlow
│   ├── audit.py              #   Session, Command, LoginLog, OperateLog
│   ├── acl.py                #   CommandFilter, LoginACL, Role, Label
│   └── extra.py              #   PublicSetting, License, OpsJob
├── services/                 # Service modules
│   ├── __init__.py           #   BaseService (generic CRUD)
│   ├── users.py              #   UsersService, GroupsService
│   ├── assets.py             #   AssetsService, CategoryService, NodesService ...
│   ├── accounts.py           #   AccountsService, TemplatesService ...
│   ├── perms.py              #   PermsService, SelfService
│   ├── auth.py               #   AuthService
│   ├── audits.py             #   AuditsService
│   ├── orgs.py               #   OrgsService
│   ├── tickets.py            #   TicketsService
│   ├── terminal.py           #   TerminalService
│   ├── settings.py           #   SettingsService
│   ├── labels.py             #   LabelsService
│   ├── acls.py               #   CommandFiltersService, LoginACLsService
│   ├── rbac.py               #   RBACService
│   ├── ops.py                #   OpsService
│   └── xpack.py              #   XpackService
├── auth.py                   # Authentication strategies
│   ├── SignatureAuth         #   HMAC-SHA256 signing
│   ├── PasswordAuth          #   Username/password → Bearer Token (auto-cache + expiry refresh)
│   ├── BearerTokenAuth       #   Bearer Token
│   └── PrivateTokenAuth      #   Private Token
├── client.py                 # Client main entry + Response
├── errors.py                 # APIError, NotFoundError, UnauthorizedError ...
└── utils/                    # Utility functions
```

## Testing

SDK includes unit tests and integration tests. Integration tests run against a real JumpServer instance.

### Prerequisites

Set the following environment variables (supports two auth methods, choose one):

```bash
# Option 1: AccessKey authentication
export JUMPSERVER_URL=https://your-jumpserver.example.com
export JUMPSERVER_KEY_ID=your-access-key-id
export JUMPSERVER_SECRET_ID=your-access-key-secret

# Option 2: Username/password authentication
export JUMPSERVER_URL=https://your-jumpserver.example.com
export JUMPSERVER_USERNAME=admin
export JUMPSERVER_PASSWORD=your-password
```

When environment variables are not set, integration tests are automatically skipped.

### Run All Tests

```bash
pip install -e ".[dev]"
pytest
```

### Run a Single Test

```bash
pytest tests/test_client.py::TestIntegrationUsers::test_profile -v
```

### Test Coverage

| Resource | Read(R) | Other | Description |
|----------|---------|-------|-------------|
| Users | ✅ | profile / list / search / offset | User query + profile |
| User Groups | ✅ | list | User group query |
| Assets | ✅ | list | Generic asset query |
| Hosts | ✅ | list | Host query |
| Databases | ✅ | list | Database query |
| Nodes | ✅ | list | Node query |
| Platforms | ✅ | list | Platform query |
| Organizations | ✅ | list | Organization query |
| Permissions | ✅ | list | Permission query |
| Audits | ✅ | list_sessions | Session query |
| Labels | ✅ | list | Label query |
| Settings | ✅ | public | Public settings query |
| Client | ✅ | auth / get / post / with_org | Connectivity + error handling |

## Development

```bash
# Clone repository
git clone https://github.com/fit2cloud-sdk/jumpserver-sdk-py.git
cd jumpserver-sdk-py

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint & type check
ruff check .
mypy jumpserver/
```

## License

MIT — see [LICENSE](./LICENSE).
