from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LoginForm, SignupForm


def user_login(request):

    if request.method == 'GET':
        form = LoginForm()

        return render(request, 'usuarios/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['Usuário']
            password = form.cleaned_data['Senha']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')

        messages.error(request, f'Usuário e/ou senha incorretos.')

        return render(request, 'usuarios/login.html', {'form': form})


def user_signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('cadastro-user')

        return render(request, 'usuarios/cadastro.html', {'form': form})

    else:
        form = SignupForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


def sign_out(request):

    logout(request)
    return redirect('index')
