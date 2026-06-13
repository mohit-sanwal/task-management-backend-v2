from rest_framework.exceptions import ValidationError


def validate_ticket_title(title):

    if len(title.strip()) < 5:
        raise ValidationError(
            "Title must be at least 5 characters long"
        )