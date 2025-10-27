from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        SUPERVISOR = "supervisor", "Supervisor"
        OPERATOR = "operator", "Operator"

    role = models.CharField(
        max_length=32,
        choices=Roles.choices,
        default=Roles.OPERATOR,
        help_text="Role determines permissions in the system.",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

from django.db import models

# Create your models here.
