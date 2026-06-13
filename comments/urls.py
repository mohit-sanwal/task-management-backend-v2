from django.urls import path

from .views import (
    CreateCommentView,
    TicketCommentsView,
    UpdateCommentView,
    DeleteCommentView,
)

urlpatterns = [

    path(
        "comments",
        CreateCommentView.as_view()
    ),

    path(
        "comments/<int:ticket_id>",
        TicketCommentsView.as_view()
    ),

    path(
        "comments/<int:comment_id>/update",
        UpdateCommentView.as_view()
    ),

    path(
        "comments/<int:comment_id>/delete",
        DeleteCommentView.as_view()
    ),
]