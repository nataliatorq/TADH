import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class BaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='baseuser_set',  # Nome exclusivo para evitar conflitos
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='baseuser_set',  # Nome exclusivo para evitar conflitos
        blank=True,
        help_text='Specific permissions for this user.'
    )