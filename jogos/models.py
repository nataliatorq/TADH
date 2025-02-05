import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="users/images/%Y/%m/%d/", blank=True, null=True)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


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
    user = models.OneToOneField("jogos.BaseUser", on_delete=models.SET_NULL, related_name="customer", null=True)

    def __str__(self):
        return self.user.username


class Offensiva(models.Model):
    user = models.OneToOneField("jogos.BaseUser", on_delete=models.SET_NULL, related_name="offensiva", null=True)
    streak = models.PositiveIntegerField(default=0)  
    last_interaction = models.DateField(null=True, blank=True)
  