from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    Usuário = forms.CharField(max_length=150)
    Senha = forms.CharField(max_length=150, widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    