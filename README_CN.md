[![EN](https://img.shields.io/badge/EN-English-blue)](README.md)
[![CN](https://img.shields.io/badge/CN-中文-red)](README_CN.md)

# jumpserver-sdk-py

[JumpServer](https://www.jumpserver.org/) REST API 的 Python SDK，兼容 **v4.10.x**。

[English](README.md) | [中文文档](README_CN.md)

## 功能特性

- **v4 支持** — SDK 面向 JumpServer v4.x
- **完整 CRUD 服务** — 用户、资产、账号、权限、组织、工单、自服务、运维任务等
- **分类资产** — 主机、网络设备、数据库、Web、云、自定义
- **多种认证方式** — AccessKey (HMAC-SHA256)、密码认证 (Bearer Token 自动缓存)、Private Token、Bearer Token、自定义 Authenticator
- **密码认证自动缓存** — 首次请求通过用户名密码换取 Bearer Token，自动缓存并根据过期时间提前 5 分钟刷新，401 时自动重新获取
- **组织切换** — `with_org(id)` 切换组织上下文
- **自动分页** — 支持 `limit` / `offset` 分页参数，`limit` 默认 `10` 避免全量拉取
- **增强错误信息** — 从 `{"field": ["msg"]}` 和嵌套序列化器中自动提取字段级错误
- **智能重试** — 指数退避 + 随机抖动，仅重试瞬时错误 (408/429/5xx)
- **丰富平台模型** — PlatformProtocol 协议详情（含 secret_types, port_from_addr, setting 等）
- **类型安全** — 全量 dataclass 模型，支持 IDE 自动补全

## 环境要求

- Python 3.9+

## 安装

```bash
pip install jumpserver-sdk
```

## 快速开始

```python
from jumpserver import Client

# 使用 AccessKey 创建客户端（推荐服务账号使用）
client = Client(
    base_url="https://jumpserver.example.com",
    access_key="your-access-key-id",
    access_secret="your-access-key-secret",
)

# 使用用户名/密码创建客户端（自动换取 Bearer Token 并缓存）
client = Client(
    base_url="https://jumpserver.example.com",
    username="admin",
    password="password",
)

# 使用 Private Token
client = Client(
    base_url="https://jumpserver.example.com",
    token="your-private-token",
)

# 获取当前用户信息
user, resp = client.users.profile()
print(user.name, user.username)

# 查询用户列表
users, resp = client.users.list(limit=20)
for u in users:
    print(u.username, u.email)

# 创建主机资产
from jumpserver.models.asset import AssetRequest

asset, resp = client.hosts.create(AssetRequest(
    name="web-01",
    address="192.168.1.10",
    platform=1,
))
print("创建成功:", asset.id)

# 切换组织上下文
org_client = client.with_org("org-id-here")
org_client.assets.list()
```

## 认证方式

```python
# AccessKey HMAC-SHA256（推荐服务账号使用）
client = Client(
    base_url="https://jumpserver.example.com",
    access_key="key-id",
    access_secret="secret-id",
)

# 用户名密码认证
# 首次请求自动 POST /api/v1/authentication/auth/ 获取 Bearer Token
# Token 自动缓存，过期前 5 分钟自动刷新，收到 401 时自动重新获取
client = Client(
    base_url="https://jumpserver.example.com",
    username="admin",
    password="password",
)

# Bearer Token（静态）
client = Client(
    base_url="https://jumpserver.example.com",
    bearer_token="your-bearer-token",
)

# Private Token（静态，Authorization: Token <token>）
client = Client(
    base_url="https://jumpserver.example.com",
    token="your-private-token",
)

# 自定义 Authenticator
from jumpserver.auth import Authenticator
from requests import PreparedRequest

class MyAuth(Authenticator):
    def __call__(self, request: PreparedRequest) -> None:
        request.headers["X-Custom-Auth"] = "my-secret"
```

### 密码认证流程

```
首次请求 → POST /api/v1/authentication/auth/ {"username": "...", "password": "..."}
         ← 返回 {"token": "...", "date_expired": "2026/07/03 11:48:25 +0800"}
         → 缓存 token 及过期时间
         → 设置 Authorization: Bearer <token>

后续请求 → 检查缓存：
           token 存在 且 距过期 > 5 分钟 → 复用缓存
           否则 → 重新获取 token

收到 401  → 清空缓存 → 重新获取 token → 重试一次
```

## 错误处理

```python
from jumpserver.errors import APIError, NotFoundError, is_not_found

try:
    user, resp = client.users.get("non-existent-id")
except NotFoundError as e:
    print("未找到 (404):", e)
except APIError as e:
    print(f"API 错误 {e.status_code}: {e}")
```

## 服务列表

| 服务 | 客户端字段 | 方法 | 说明 |
|------|-----------|------|------|
| 用户 | `client.users` | list / get / profile / create / update / replace / delete / invite | 用户 CRUD + 个人信息 |
| 用户组 | `client.user_groups` | list / get / create / update / delete / bind_users / list_users | 用户组 CRUD + 成员管理 |
| 角色 | `client.roles` | list(scope) / get(scope) | 组织/系统角色查询 |
| 资产 | `client.assets` | list / get / delete / perm_users | 通用资产操作 |
| 主机 | `client.hosts` | list / get / create / update / delete | 主机 CRUD |
| 网络设备 | `client.devices` | list / get / create / update / delete | 网络设备 CRUD |
| 数据库 | `client.databases` | list / get / create / update / delete | 数据库 CRUD |
| Web | `client.webs` | list / get / create / update / delete | Web 资产 CRUD |
| 云资产 | `client.clouds` | list / get / create / update / delete | 云资产 CRUD |
| 自定义 | `client.customs` | list / get / create / update / delete | 自定义资产 CRUD |
| 节点 | `client.nodes` | list / get / create / delete / create_child / get_children / children_tree | 资产树节点 CRUD + 子节点 + 树列表 |
| 平台 | `client.platforms` | list / get | 平台模板查询 |
| 区域 | `client.zones` | list / get / create / update / delete | 区域 CRUD |
| 网关 | `client.gateways` | list / get / create / update / delete | 网关 CRUD |
| 标签 | `client.labels` | list / get / create / update / delete | 标签 CRUD |
| 账号 | `client.accounts` | list / get / create / update / delete / get_secret / create_bulk / verify | 账号 CRUD + 密码查看 + 批量创建 |
| 账号模板 | `client.account_templates` | list / get / create / update / delete | 模板 CRUD |
| 改密 | `client.change_secrets` | list / get / create / update / delete / execute | 改密自动化 CRUD + 执行 |
| 账号备份 | `client.account_backups` | list / get / create / update / delete / execute | 备份计划 CRUD + 执行 |
| 组织 | `client.organizations` | list / get / create / update / delete | 组织 CRUD |
| 授权 | `client.permissions` | list / get / create / update / delete / add_users_relations / add_user_groups_relations / add_assets_relations / add_nodes_relations / get_self_asset_accounts | 资产授权 CRUD + 授权关系 + 自服务账号查询 |
| 命令过滤 | `client.command_filters` | list / get / create / update / delete / list_groups / get_group / create_group / update_group / delete_group | 命令过滤器 + 命令组 CRUD |
| 登录限制 | `client.login_acls` | list / get / delete | 登录 ACL 查询 |
| 审计 | `client.audits` | list_sessions / list_commands / list_ftp_logs / list_login_logs / list_operate_logs / get_session / download_replay | 会话、命令、FTP、登录、操作日志 |
| 认证 | `client.auth` | create_token / create_connection_token / create_super_connection_token / sso_login_url | 登录、令牌、SSO |
| 终端 | `client.terminal` | register / config / heartbeat / connect_methods / get_task | 终端注册、配置、心跳 |
| 工单 | `client.tickets` | list / get / create / approve / reject / list_flows / update_flow | 工单 CRUD + 审批 + 流程 |
| 设置 | `client.settings` | public / list | 系统设置查询 |
| 自服务 | `client.self` | list_assets / get_asset | 自服务授权资产（`client.self_service` 向后兼容） |
| 运维 | `client.ops` | run_job / get_job_result | 运维任务执行（/api/v1/ops/jobs/） |
| Xpack | `client.xpack` | license | 许可证信息 |

### 公共工具函数

| 函数 | 模块 | 说明 |
|------|------|------|
| `from_dict` | `jumpserver` | 将 JSON 字典转换为类型化的 dataclass 实例（驼峰 ↔ 下划线） |
| `format_path` | `jumpserver.utils` | 格式化 URL 路径模板 |
| `map_error` | `jumpserver.errors` | 将 HTTP 状态码映射为异常 |
| `is_not_found`, `is_unauthorized`, `is_forbidden`, `is_rate_limited` | `jumpserver.errors` | 异常类型判断 |


## 包结构

```
jumpserver/
├── models/                   # 响应 & 请求模型 (dataclass) — 每个文件均导出 __all__
│   ├── user.py               #   User, UserRequest, Group, GroupRequest
│   ├── asset.py              #   Asset, AssetRequest
│   ├── asset_extras.py       #   Node, Platform, PlatformProtocol, Zone, Gateway
│   ├── account.py            #   Account, AccountTemplate, ChangeSecret
│   ├── permission.py         #   AssetPermission, SelfAsset
│   ├── org.py                #   Organization
│   ├── auth.py               #   Token, TokenRequest, ConnectionToken
│   ├── ticket.py             #   Ticket, TicketFlow
│   ├── audit.py              #   Session, Command, LoginLog, OperateLog
│   ├── acl.py                #   CommandFilter, LoginACL, Role, Label
│   └── extra.py              #   PublicSetting, License, OpsJob
├── services/                 # 服务模块
│   ├── __init__.py           #   BaseService (通用 CRUD)
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
├── auth.py                   # 认证策略
│   ├── SignatureAuth         #   HMAC-SHA256 签名
│   ├── PasswordAuth          #   用户名密码 → Bearer Token（自动缓存+过期刷新）
│   ├── BearerTokenAuth       #   Bearer Token
│   └── PrivateTokenAuth      #   Private Token
├── client.py                 # Client 主客户端 + Response
├── py.typed                  # PEP 561 类型标记（发布类型信息）
├── errors.py                 # APIError, NotFoundError, UnauthorizedError ...
└── utils/                    # 工具函数
    └── __init__.py           #   format_path
```

## 测试

SDK 包含单元测试和集成测试。集成测试运行在真实的 JumpServer 实例上。

### 前置条件

设置以下环境变量（支持两种认证方式，二选一）：

```bash
# 方式一：AccessKey 认证
export JUMPSERVER_URL=https://your-jumpserver.example.com
export JUMPSERVER_KEY_ID=your-access-key-id
export JUMPSERVER_SECRET_ID=your-access-key-secret

# 方式二：用户名密码认证
export JUMPSERVER_URL=https://your-jumpserver.example.com
export JUMPSERVER_USERNAME=admin
export JUMPSERVER_PASSWORD=your-password
```

当环境变量未设置时，集成测试自动跳过。

### 运行全部测试

```bash
pip install -e ".[dev]"
pytest
```

### 运行单个测试

```bash
pytest tests/test_client.py::TestIntegrationUsers::test_profile -v
```

### 测试覆盖

| 资源 | 查询(R) | 其他 | 说明 |
|------|---------|------|------|
| 用户 | ✅ | profile / list / search / offset | 用户查询 + 个人信息 |
| 用户组 | ✅ | list | 用户组查询 |
| 资产 | ✅ | list | 通用资产查询 |
| 主机 | ✅ | list | 主机查询 |
| 数据库 | ✅ | list | 数据库查询 |
| 节点 | ✅ | list | 节点查询 |
| 平台 | ✅ | list | 平台查询 |
| 组织 | ✅ | list | 组织查询 |
| 权限 | ✅ | list | 授权查询 |
| 审计 | ✅ | list_sessions | 会话查询 |
| 标签 | ✅ | list | 标签查询 |
| 设置 | ✅ | public | 公共设置查询 |
| 客户端 | ✅ | auth / get / post / with_org | 连通性 + 错误处理 |

## 开发

```bash
# 克隆仓库
git clone https://github.com/fit2cloud-sdk/jumpserver-sdk-py.git
cd jumpserver-sdk-py

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查
ruff check jumpserver/ tests/
mypy jumpserver/
```

## 许可证

MIT — 阅读 [LICENSE](./LICENSE)。
