from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator

from .models import BaseUser, Jogo


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label="Senha",
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="A senha deve ter no mínimo 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial.",
            )
        ],
    )

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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas não coincidem.',
                code='invalid'
            )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ]
            }
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and BaseUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este email já está em uso.")
        return email

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
    


class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}),
        label="Nova senha",
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="A senha deve ter no mínimo 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial.",
            )
        ],
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

        if password1 != password2:
            password_confirmation_error = ValidationError(
                'As senhas não coincidem.',
                code='invalid'
            )

            raise ValidationError({
                'password1': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ]
            }
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and BaseUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este email já está em uso.")
        return email

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
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get("titulo")
        if len(titulo) < 3:
            raise ValidationError("O título deve ter pelo menos 3 caracteres.")
        if len(titulo) > 100:
            raise ValidationError("O título não pode exceder 100 caracteres.")
        return titulo

    def clean_descricao(self):
        descricao = self.cleaned_data.get("descricao")
        if len(descricao) < 10:
            raise ValidationError("A descrição deve ter pelo menos 10 caracteres.")
        return descricao

    def clean_imagem(self):
        imagem = self.cleaned_data.get("imagem")
        if imagem:
            if not imagem.content_type.startswith("image/"):
                raise ValidationError("O arquivo enviado não é uma imagem válida.")
            if imagem.size > 2 * 1024 * 1024:  # 2 MB
                raise ValidationError("O tamanho da imagem não pode exceder 2 MB.")
        return imagem

    def clean_url_jogo(self):
        url_jogo = self.cleaned_data.get("url_jogo")
        validator = URLValidator()
        try:
            validator(url_jogo)
        except ValidationError:
            raise ValidationError("A URL fornecida não é válida.")
        return url_jogo