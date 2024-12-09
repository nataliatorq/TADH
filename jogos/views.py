from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from rolepermissions.decorators import has_role_decorator

from .forms import JogoForm, UserEditForm, UserRegisterForm
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
        else:
            print(form.errors)

    return render(request, "pages/cadastro.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login efetuado com sucesso!")
            return redirect("jogos")
        else:
            messages.error(request, "Usuário ou senha inválidos!")
            return redirect("login")
    return render(request, "pages/login.html")


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def jogos_list(request):
    recentes = Jogo.objects.filter(categoria="recentes").order_by("-id")[:4]
    
    outros_list = Jogo.objects.filter(categoria="outros").order_by("-id")
    paginator = Paginator(outros_list, 10)  # Show 8 items per page
    
    page_number = request.GET.get('page', 1)
    outros = paginator.get_page(page_number)

    context = {
        "recentes": recentes, 
        "outros": outros,
        "paginator": paginator
    }
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


def sobre(request):
    return render(request, "pages/sobre.html")

def faleconosco(request):
    return render(request, "pages/faleconosco.html")

@login_required(login_url="login")
def profile(request):
    return render(request, "pages/profile.html")


@login_required(login_url="login")
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)

        try:
            dia = int(request.POST.get("day", 0))
            mes = int(request.POST.get("month", 0))
            ano = int(request.POST.get("year", 0))
            data_nascimento = date(ano, mes, dia)
            user.birth_date = data_nascimento
        except (ValueError, TypeError):
            data_nascimento = user.birth_date

        if form.is_valid():
            user = form.save(commit=False)
            user.birth_date = data_nascimento
            if "photo" in request.FILES:
                user.photo = request.FILES["photo"]
            if form.cleaned_data.get("password"):
                user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")
        else:
            messages.error(request, "Erro ao atualizar o perfil")
    else:
        form = UserEditForm(instance=user)

    return render(request, "pages/profile_edit.html", {"form": form})
