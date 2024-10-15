from datetime import date

from django.shortcuts import redirect, render

from .forms import UserRegisterForm


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

def login(request):
    return render(request, "pages/login.html")