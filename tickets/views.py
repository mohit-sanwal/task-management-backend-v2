from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Ticket
from .serializers import TicketSerializer
from .services import (
    create_ticket,
    get_ticket_by_id,
    update_ticket,
)


class CreateTicketView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():

            ticket = create_ticket(
                user=request.user,
                data=serializer.validated_data
            )

            response_serializer = TicketSerializer(ticket)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TicketListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role in ["admin", "super_admin"]:
            tickets = Ticket.objects.all()

        else:
            tickets = Ticket.objects.filter(user=user)

        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data)


class TicketDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_ticket(self, ticket_id):

        return get_ticket_by_id(
            ticket_id=ticket_id
        )

    def get(self, request, ticket_id):

        ticket = self.get_ticket(ticket_id)

        user = request.user

        if (
            user.role == "user"
            and ticket.user != user
        ):
            return Response(
                {"error": "Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TicketSerializer(ticket)

        return Response(serializer.data)

    def patch(self, request, ticket_id):

        ticket = self.get_ticket(ticket_id)

        user = request.user

        if (
            user.role == "user"
            and ticket.user != user
        ):
            return Response(
                {"error": "Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TicketSerializer(
            ticket,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_ticket = update_ticket(
                ticket=ticket,
                data=serializer.validated_data
            )

            response_serializer = TicketSerializer(
                updated_ticket
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, ticket_id):

        ticket = self.get_ticket(ticket_id)

        user = request.user

        if (
            user.role == "user"
            and ticket.user != user
        ):
            return Response(
                {"error": "Access denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        ticket.delete()

        return Response({
            "message": "Ticket deleted successfully"
        })