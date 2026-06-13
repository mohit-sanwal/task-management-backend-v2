from django.db import models
from authentication.models import User
from tickets.models import Ticket


class TicketAssignment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tickets"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_assignments"
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-assigned_at"]

    def __str__(self):

        return (
            f"{self.ticket.title} -> "
            f"{self.assigned_to.username}"
        )
