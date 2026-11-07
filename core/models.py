from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models


class Mensagens(models.Model):
    nome = models.CharField(max_length=200)
    data = models.CharField(max_length=150)
    mensagem = models.TextField()

    imagem = CloudinaryField(
        "imagem",
        blank=True,
        null=True,
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.mensagem
