from django.urls import path

from .views import (
    AssignTicketView,
    AssignmentHistoryView,
    AssignableUsersView,
)

urlpatterns = [

    path(
        "assign-ticket",
        AssignTicketView.as_view()
    ),

    path(
        "assignment-history/<int:ticket_id>",
        AssignmentHistoryView.as_view()
    ),

    path(
        "assignable-users",
        AssignableUsersView.as_view()
    ),
]