from django import forms
from django.core.exceptions import ValidationError

from .models import BaseUser, Jogo


class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'})
    )

    class Meta:
        model = BaseUser
        fields = ('username', 'email', 'password', 'password2', 'birth_date', 'photo')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crie uma senha'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'placeholder': 'Adicionar nova foto form-input'}),
        }
    


class UserEditForm(forms.ModelForm):

    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}),
        label="Nova senha",
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}),
        label="Confirmação da nova senha",
    )


    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'password1', 'password2', 'birth_date', 'photo']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Nome'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-input', 'placeholder': 'Email'}
            ),
            'password1': forms.PasswordInput(
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
            if not password1 or not password2:
                raise forms.ValidationError("Ambos os campos de senha devem ser preenchidos.")
            if password1 != password2:
                raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data


    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and BaseUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

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