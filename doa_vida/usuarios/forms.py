from django import forms

class LoginForm(forms.Form):
    Usuário = forms.CharField(max_length=150)
    Senha = forms.CharField(max_length=150, widget=forms.PasswordInput)

