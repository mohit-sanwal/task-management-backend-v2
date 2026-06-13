from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket

        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]