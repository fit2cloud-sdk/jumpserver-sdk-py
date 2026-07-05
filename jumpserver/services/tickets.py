"""Tickets service."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from jumpserver.models.ticket import Ticket, TicketFlow, TicketFlowRequest, TicketRequest
from jumpserver.services import BaseService, from_dict

if TYPE_CHECKING:
    from jumpserver.client import Response



__all__ = ["TicketsService"]

class TicketsService(BaseService):
    """CRUD for /api/v1/tickets/."""
    list_url = "/api/v1/tickets/tickets/"
    detail_url = "/api/v1/tickets/tickets/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[Ticket], Response]:
        return self._list(Ticket, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[Ticket], Response]:
        return self._get(Ticket, id)

    def create(self, req: TicketRequest) -> tuple[Optional[Ticket], Response]:
        return self._create(Ticket, req)

    def approve(self, id: str, action: str = "approve"):
        _, resp = self._client.post(f"/api/v1/tickets/tickets/{id}/approve/", {"action": action})
        return resp

    def reject(self, id: str):
        return self.approve(id, action="reject")

    def list_flows(self, limit: int = 10, offset: Optional[int] = None) -> tuple[list[TicketFlow], Response]:
        params = {}
        params["limit"] = limit if limit is not None else 10
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/tickets/flows/", params=params or None)

        results = (data or {}).get("results", [])
        return [from_dict(TicketFlow, item) for item in results], resp

    def update_flow(self, id: str, req: TicketFlowRequest) -> tuple[Optional[TicketFlow], Response]:
        from jumpserver.utils import format_path

        data, resp = self._client.patch(format_path("/api/v1/tickets/flows/%s/", id), req)
        return from_dict(TicketFlow, data) if data else None, resp
