"""Accounts, Templates, ChangeSecret, Backup services."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from jumpserver.client import Response

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
from jumpserver.services import BaseService, from_dict
from jumpserver.utils import format_path

__all__ = ["AccountsService", "TemplatesService", "ChangeSecretService", "BackupService"]


class AccountsService(BaseService):
    """CRUD for /api/v1/accounts/accounts/."""

    list_url = "/api/v1/accounts/accounts/"
    detail_url = "/api/v1/accounts/accounts/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[Account], Response]:
        return self._list(Account, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[Account], Response]:
        return self._get(Account, id)

    def create(self, req: AccountRequest) -> tuple[Optional[Account], Response]:
        return self._create(Account, req)

    def update(self, id: str, req: AccountRequest) -> tuple[Optional[Account], Response]:
        return self._update(Account, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)

    def get_secret(self, id: str):
        url = format_path("/api/v1/accounts/account-secrets/%s/", id)
        data, resp = self._client.get(url)
        return from_dict(Account, data) if data else None, resp

    def create_bulk(self, reqs: list[AccountRequest]) -> Response:
        _, resp = self._client.post("/api/v1/accounts/accounts/bulk/", reqs)
        return resp

    def create_bulk_by_template(self, req) -> Response:
        _, resp = self._client.post("/api/v1/accounts/accounts/bulk/", req)
        return resp

    def verify(self, id: str):
        url = format_path("/api/v1/accounts/accounts/%s/verify/", id)
        data, resp = self._client.get(url)
        return from_dict(AccountVerifyResult, data) if data else None, resp

    def create_verify_task(self, req: AccountVerifyTaskRequest):
        data, resp = self._client.post("/api/v1/accounts/accounts/verify/", req)
        return from_dict(AccountVerifyTask, data) if data else None, resp


class TemplatesService(BaseService):
    """CRUD for /api/v1/accounts/account-templates/."""

    list_url = "/api/v1/accounts/account-templates/"
    detail_url = "/api/v1/accounts/account-templates/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[AccountTemplate], Response]:
        return self._list(AccountTemplate, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[AccountTemplate], Response]:
        return self._get(AccountTemplate, id)

    def create(self, req: AccountTemplateRequest) -> tuple[Optional[AccountTemplate], Response]:
        return self._create(AccountTemplate, req)

    def update(self, id: str, req: AccountTemplateRequest) -> tuple[Optional[AccountTemplate], Response]:
        return self._update(AccountTemplate, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)


class ChangeSecretService(BaseService):
    """CRUD for /api/v1/accounts/change-secret-automations/."""

    list_url = "/api/v1/accounts/change-secret-automations/"
    detail_url = "/api/v1/accounts/change-secret-automations/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[ChangeSecretAutomation], Response]:
        return self._list(ChangeSecretAutomation, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[ChangeSecretAutomation], Response]:
        return self._get(ChangeSecretAutomation, id)

    def create(self, req: ChangeSecretAutomationRequest) -> tuple[Optional[ChangeSecretAutomation], Response]:
        return self._create(ChangeSecretAutomation, req)

    def update(self, id: str, req: ChangeSecretAutomationRequest) -> tuple[Optional[ChangeSecretAutomation], Response]:
        return self._update(ChangeSecretAutomation, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)

    def execute(self, id: str) -> Response:
        """Execute the change-secret automation immediately."""
        _, resp = self._client.post(
            format_path("/api/v1/accounts/change-secret-automations/%s/execute/", id)
        )
        return resp


class BackupService(BaseService):
    """CRUD for /api/v1/accounts/account-backup-plans/."""

    list_url = "/api/v1/accounts/account-backup-plans/"
    detail_url = "/api/v1/accounts/account-backup-plans/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[AccountBackupPlan], Response]:
        return self._list(AccountBackupPlan, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[AccountBackupPlan], Response]:
        return self._get(AccountBackupPlan, id)

    def create(self, req: AccountBackupPlanRequest) -> tuple[Optional[AccountBackupPlan], Response]:
        return self._create(AccountBackupPlan, req)

    def update(self, id: str, req: AccountBackupPlanRequest) -> tuple[Optional[AccountBackupPlan], Response]:
        return self._update(AccountBackupPlan, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)

