from django.db import models
from django.conf import settings


class Ticket(models.Model):

    STATUS_CHOICES = (
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("IN_REVIEW", "In Review"),
        ("IN_QE", "In QE"),
        ("DONE", "Done"),
    )

    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="LOW"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title