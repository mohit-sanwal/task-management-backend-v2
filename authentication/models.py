# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
        ("super_admin", "Super Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )

    can_assign = models.BooleanField(default=False)

    def __str__(self):
        return self.username