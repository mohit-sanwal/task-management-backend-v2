from .models import Ticket
from .validators import validate_ticket_title
from django.shortcuts import get_object_or_404


def create_ticket(*, user, data):

    validate_ticket_title(data["title"])

    ticket = Ticket.objects.create(
        title=data["title"],
        description=data.get("description", ""),
        priority=data.get("priority", "LOW"),
        user=user
    )

    return ticket


def get_ticket_by_id(*, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    return ticket


def update_ticket(*, ticket, data):

    if "title" in data:
        ticket.title = data["title"]

    if "description" in data:
        ticket.description = data["description"]

    if "priority" in data:
        ticket.priority = data["priority"]

    if "status" in data:
        ticket.status = data["status"]

    ticket.save()

    return ticket