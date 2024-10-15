from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.user_register, name="cadastro"),
    path("login/", views.login, name="login"),
]
