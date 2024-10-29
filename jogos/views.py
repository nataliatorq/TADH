from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rolepermissions.decorators import has_role_decorator

from .forms import JogoForm, UserRegisterForm
from .models import Jogo


def home(request):
    return render(request, "pages/home.html")


def user_register(request):
    if request.method == "GET":
        form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        dia = int(request.POST.get("day"))
        mes = int(request.POST.get("month"))
        ano = int(request.POST.get("year"))
        data_nascimento = date(ano, mes, dia)
        form.birth_date = data_nascimento
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect("login")

    return render(request, "pages/cadastro.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("jogos")
        else:
            return redirect("login")
    return render(request, "pages/login.html")


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def jogos_list(request):
    recentes = Jogo.objects.filter(categoria="recentes").order_by("-id")[:4]
    outros = Jogo.objects.filter(categoria="outros").order_by("-id")[:10]

    context = {"recentes": recentes, "outros": outros}
    return render(request, "pages/jogos.html", context)


@login_required(login_url="login")
@has_role_decorator("Admin")
def criar_jogo(request):
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("jogos")
    else:
        form = JogoForm()
    return render(request, "pages/jogo-form.html", {"form": form})


@login_required(login_url="login")
@has_role_decorator("Admin")
def editar_jogo(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    if request.method == "POST":
        form = JogoForm(request.POST, request.FILES, instance=jogo)
        if form.is_valid():
            form.save()
            return redirect("jogos")
    else:
        form = JogoForm(instance=jogo)
    return render(request, "pages/jogo-form.html", {"form": form, "jogo": jogo})


@login_required(login_url="login")
@has_role_decorator("Admin")
def remover_jogo(request, id):
    jogo = get_object_or_404(Jogo, id=id)
    jogo.delete()
    return redirect("jogos")
