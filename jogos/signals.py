from datetime import timedelta

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Offensiva


@receiver(user_logged_in)
def atualizar_offensiva_login(sender, request, user, **kwargs):
    # Atualiza a ofensiva no login
    ofensiva, created = Offensiva.objects.get_or_create(user=user)
    hoje = now().date()

    if ofensiva.last_interaction == hoje:
        # Já atualizou hoje, não faz nada
        return

    if ofensiva.last_interaction == hoje - timedelta(days=1):
        # Incrementa a streak se o último login foi ontem
        ofensiva.streak += 1
    else:
        # Reseta a streak se houve um intervalo maior que 1 dia
        ofensiva.streak = 1

    # Atualiza a data da última interação
    ofensiva.last_interaction = hoje
    ofensiva.save()
