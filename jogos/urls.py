from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.user_register, name="cadastro"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("jogos/", views.jogos_list, name="jogos"),
    path("jogos/criar/", views.criar_jogo, name="criar_jogo"),
    path("jogos/editar/<int:id>/", views.editar_jogo, name="editar_jogo"),
    path("jogos/remover/<int:id>/", views.remover_jogo, name="deletar_jogo"),
    path("sobre/", views.sobre, name="sobre"),
    path("faleconosco/", views.faleconosco, name="faleconosco"),
]
