from django.shortcuts import get_object_or_404
from .models import User


def update_user_role(*, user_id, role):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.role = role

    user.save()

    return user


def delete_user(*, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.delete()