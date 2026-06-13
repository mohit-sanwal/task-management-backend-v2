from .models import TicketAssignment
from tickets.models import Ticket
from authentication.models import User

from django.shortcuts import get_object_or_404


def assign_ticket(
    *,
    ticket_id,
    assigned_by,
    assigned_to_id
):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    assigned_to = get_object_or_404(
        User,
        id=assigned_to_id
    )

    assignment = TicketAssignment.objects.create(
        ticket=ticket,
        assigned_by=assigned_by,
        assigned_to=assigned_to
    )

    return assignment