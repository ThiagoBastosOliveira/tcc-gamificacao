from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=65)
    senha = forms.CharField(max_length=65, widget=forms.PasswordInput)

