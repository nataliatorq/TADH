import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class BaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="users/images/%Y/%m/%d/", blank=True, default="")

    USERNAME_FIELD = "username"


class Jogo(models.Model):
    CATEGORIAS = [
        ("recentes", "Recentes"),
        ("outros", "Outros"),
    ]
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to="jogos/")
    url_jogo = models.URLField()
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default="outros")

    def __str__(self):
        return self.titulo


class Customer(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Offensiva(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="offensiva")
    streak = models.PositiveIntegerField(default=0)  
    last_interaction = models.DateField(null=True, blank=True)
  