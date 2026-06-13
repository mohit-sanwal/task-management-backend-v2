from django.urls import path

from .views import (
    CreateTicketView,
    TicketListView,
    TicketDetailView,
)

urlpatterns = [
    path("create-ticket", CreateTicketView.as_view()),
    path("tickets", TicketListView.as_view()),
    path("tickets/<int:ticket_id>", TicketDetailView.as_view()),
]