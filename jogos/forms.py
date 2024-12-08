from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
    


class UserEditForm(UserCreationForm):

    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Nova senha'}
        ),
        label="Nova senha",
    )
    password2 = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Nova senha'}
        ),
        label="Confirmação da nova senha",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'birth_date', 'photo']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Nome'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Email'}
            ),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Senha'}
            ),
            'password2': forms.PasswordInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Confirme sua senha'}
            ),
            'birth_date': forms.DateInput(
                attrs={'class': 'form-control form-input'}
            ),
            'photo': forms.FileInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Adicionar nova foto'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget.attrs, 'class'):
                field.widget.attrs.update({'class': 'form-control form-input'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        
        if password1:
            user.set_password(password1)
        
        if commit:
            user.save()
        return user


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