# JumpServer Python SDK

Python SDK for the [JumpServer](https://github.com/jumpserver/jumpserver) API.

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

# Using username/password
client = Client(
    base_url="https://jumpserver.example.com",
    username="admin",
    password="password",
)

# Using private token
client = Client(
    base_url="https://jumpserver.example.com",
    token="your-private-token",
)

# Get current user profile
user = client.users.profile()
print(user.name, user.username)

# List assets
assets, pagination = client.assets.list()
for asset in assets:
    print(asset.name, asset.address)

# Create an asset
from jumpserver.models import AssetRequest

asset, _ = client.databases.create(AssetRequest(
    name="db01",
    address="10.0.0.1",
    platform=22,
    protocols=[{"name": "mysql", "port": 3306}],
))

# Switch organization scope
org_client = client.with_org("org-id-here")
org_client.assets.list()
```

## Documentation

See [JumpServer API Documentation](https://docs.jumpserver.org/) for available endpoints.

## Development

```bash
pip install -e ".[dev]"
pytest
```
