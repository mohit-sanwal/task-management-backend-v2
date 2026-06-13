from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from authentication.models import User
from .models import TicketAssignment
from .serializers import (
    TicketAssignmentSerializer
)
from .services import assign_ticket


class AssignTicketView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if user.role not in [
            "admin",
            "super_admin"
        ]:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        ticket_id = request.data.get("ticket_id")

        assigned_to_id = request.data.get(
            "assigned_to"
        )

        assignment = assign_ticket(
            ticket_id=ticket_id,
            assigned_by=user,
            assigned_to_id=assigned_to_id
        )

        serializer = TicketAssignmentSerializer(
            assignment
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class AssignmentHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):

        assignments = (
            TicketAssignment.objects
            .filter(ticket_id=ticket_id)
        )

        serializer = TicketAssignmentSerializer(
            assignments,
            many=True
        )

        return Response(serializer.data)


class AssignableUsersView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.filter(
            role__in=["admin", "user"]
        )

        data = []

        for user in users:

            data.append({
                "id": user.id,
                "username": user.username,
                "role": user.role
            })

        return Response(data)