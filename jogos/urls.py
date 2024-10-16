from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.user_register, name="cadastro"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("jogos/", views.jogos_list, name="jogos"),
]
