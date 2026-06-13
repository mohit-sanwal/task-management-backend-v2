from rest_framework import serializers
from .models import TicketAssignment


class TicketAssignmentSerializer(
    serializers.ModelSerializer
):

    assigned_by_username = serializers.CharField(
        source="assigned_by.username",
        read_only=True
    )

    assigned_to_username = serializers.CharField(
        source="assigned_to.username",
        read_only=True
    )

    class Meta:

        model = TicketAssignment

        fields = [
            "id",
            "ticket",
            "assigned_by",
            "assigned_to",
            "assigned_by_username",
            "assigned_to_username",
            "assigned_at",
        ]

        read_only_fields = [
            "assigned_by",
            "assigned_at",
        ]