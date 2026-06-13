from django.shortcuts import get_object_or_404

from .models import Comment
from tickets.models import Ticket


def create_comment(
    *,
    ticket_id,
    user,
    content,
    parent_id=None
):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    parent = None

    if parent_id:

        parent = get_object_or_404(
            Comment,
            id=parent_id
        )

    comment = Comment.objects.create(
        ticket=ticket,
        user=user,
        content=content,
        parent=parent
    )

    return comment


def soft_delete_comment(*, comment):

    comment.is_deleted = True

    comment.content = "[deleted]"

    comment.save()