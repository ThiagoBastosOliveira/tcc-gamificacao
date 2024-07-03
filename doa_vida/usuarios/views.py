from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LoginForm


def sign_in(request):

    if request.method == 'GET':
        form = LoginForm()
        context = {'form': form}

        return render(request, 'usuarios/login.html', context)

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['Usuário']
            password = form.cleaned_data['Senha']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

        context = {'form': form}
        messages.error(request, f'Usuário e/ou senha incorretos.')

        return render(request, 'usuarios/login.html', context)


def sign_out(request):
    logout(request)

    return redirect('login')


def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            form.save()
            return redirect('login')

        return render(request, 'usuarios/cadastro.html', context)

    else:
        form = UserCreationForm()
        context = {'form': form}

    return render(request, 'usuarios/cadastro.html', context)
