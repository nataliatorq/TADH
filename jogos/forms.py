from django import forms
from django.contrib.auth import get_user_model

from .models import Jogo

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-input', 'placeholder': 'Confirme sua senha'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'birth_date', 'photo')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-input', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-input', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-input', 'placeholder': 'Crie uma senha'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control    form-input'}),
            'photo': forms.FileInput(attrs={'placeholder': 'Adicionar nova foto form-input'}),
        }


class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ['titulo', 'descricao', 'imagem', 'url_jogo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'descrição'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'url_jogo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type the game url here'}),
        }