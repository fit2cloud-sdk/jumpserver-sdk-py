"""Accounts, Templates, ChangeSecret, Backup services."""

from __future__ import annotations

from typing import Optional

from jumpserver.client import Client, Response
from jumpserver.models.account import (
    Account,
    AccountBackupPlan,
    AccountBackupPlanRequest,
    AccountRequest,
    AccountTemplate,
    AccountTemplateRequest,
    AccountVerifyResult,
    AccountVerifyTask,
    AccountVerifyTaskRequest,
    ChangeSecretAutomation,
    ChangeSecretAutomationRequest,
)
from jumpserver.services import BaseService
from jumpserver.utils import format_path

__all__ = ["AccountsService", "TemplatesService", "ChangeSecretService", "BackupService"]


class AccountsService(BaseService):
    """CRUD for /api/v1/accounts/accounts/."""

    list_url = "/api/v1/accounts/accounts/"
    detail_url = "/api/v1/accounts/accounts/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(Account, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(Account, id)

    def create(self, req: AccountRequest):
        return self._create(Account, req)

    def update(self, id: str, req: AccountRequest):
        return self._update(Account, id, req)

    def delete(self, id: str):
        return self._delete(id)

    def get_secret(self, id: str):
        url = format_path("/api/v1/accounts/account-secrets/%s/", id)
        data, resp = self._client.get(url)
        return _from_dict(Account, data) if data else None, resp

    def create_bulk(self, reqs: list[AccountRequest]):
        _, resp = self._client.post("/api/v1/accounts/accounts/bulk/", reqs)
        return resp

    def create_bulk_by_template(self, req):
        _, resp = self._client.post("/api/v1/accounts/accounts/bulk/", req)
        return resp

    def verify(self, id: str):
        url = format_path("/api/v1/accounts/accounts/%s/verify/", id)
        data, resp = self._client.get(url)
        return _from_dict(AccountVerifyResult, data) if data else None, resp

    def create_verify_task(self, req: AccountVerifyTaskRequest):
        data, resp = self._client.post("/api/v1/accounts/accounts/verify/", req)
        return _from_dict(AccountVerifyTask, data) if data else None, resp


class TemplatesService(BaseService):
    """CRUD for /api/v1/accounts/templates/."""

    list_url = "/api/v1/accounts/templates/"
    detail_url = "/api/v1/accounts/templates/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(AccountTemplate, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(AccountTemplate, id)

    def create(self, req: AccountTemplateRequest):
        return self._create(AccountTemplate, req)

    def update(self, id: str, req: AccountTemplateRequest):
        return self._update(AccountTemplate, id, req)

    def delete(self, id: str):
        return self._delete(id)


class ChangeSecretService(BaseService):
    """CRUD for /api/v1/accounts/change-secret-automations/."""

    list_url = "/api/v1/accounts/change-secret-automations/"
    detail_url = "/api/v1/accounts/change-secret-automations/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(ChangeSecretAutomation, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(ChangeSecretAutomation, id)

    def create(self, req: ChangeSecretAutomationRequest):
        return self._create(ChangeSecretAutomation, req)

    def update(self, id: str, req: ChangeSecretAutomationRequest):
        return self._update(ChangeSecretAutomation, id, req)

    def delete(self, id: str):
        return self._delete(id)


class BackupService(BaseService):
    """CRUD for /api/v1/accounts/backup-plans/."""

    list_url = "/api/v1/accounts/backup-plans/"
    detail_url = "/api/v1/accounts/backup-plans/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(AccountBackupPlan, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(AccountBackupPlan, id)

    def create(self, req: AccountBackupPlanRequest):
        return self._create(AccountBackupPlan, req)

    def update(self, id: str, req: AccountBackupPlanRequest):
        return self._update(AccountBackupPlan, id, req)

    def delete(self, id: str):
        return self._delete(id)


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
