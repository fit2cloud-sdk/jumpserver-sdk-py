"""Tickets service."""

from typing import Optional

from jumpserver.client import Client, Response
from jumpserver.models.ticket import Ticket, TicketFlow, TicketFlowRequest, TicketRequest
from jumpserver.services import BaseService

__all__ = ["TicketsService"]


class TicketsService(BaseService):
    """CRUD for /api/v1/tickets/."""

    list_url = "/api/v1/tickets/tickets/"
    detail_url = "/api/v1/tickets/tickets/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(Ticket, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(Ticket, id)

    def create(self, req: TicketRequest):
        return self._create(Ticket, req)

    def approve(self, id: str, action: str = "approve"):
        _, resp = self._client.post(
            f"/api/v1/tickets/tickets/{id}/approve/", {"action": action}
        )
        return resp

    def reject(self, id: str):
        return self.approve(id, action="reject")

    def list_flows(self, limit=None, offset=None):
        return self._list(TicketFlow, limit=limit, offset=offset)

    def update_flow(self, id: str, req: TicketFlowRequest):
        return self._update(TicketFlow, id, req)
