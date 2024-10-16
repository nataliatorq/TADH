from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserRegisterForm
from .models import Jogo


def home(request):
    return render(request, "pages/home.html")

def user_register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        dia = int(request.POST.get('day'))
        mes = int(request.POST.get('month'))
        ano = int(request.POST.get('year'))
        data_nascimento = date(ano, mes, dia)
        form.birth_date=data_nascimento
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, "pages/cadastro.html", {'form': form})

def user_login(request):
    if request.method == "POST":
        # Obtem os dados enviados pelo Usuário
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Tenta autenticar o Usuário (Se não conseguir, retorna None)
        user = authenticate(username=username, password=password)
        if user:
            # Realiza o login do Usuário já autenticado.
            login(request, user)
            return redirect("jogos")
        else:
            return redirect("login")
    return render(request, "pages/login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def jogos_list(request):
    recentes = Jogo.objects.filter(categoria='recentes').order_by('-id')[:4]
    outros = Jogo.objects.filter(categoria='outros').order_by('-id')[:8]
    
    context = {
        'recentes': recentes,
        'outros': outros
    }
    return render(request, 'pages/jogos.html', context)