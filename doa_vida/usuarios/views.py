from django.contrib.auth import login, logout, authenticate
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
            username = form.cleaned_data['user']
            password = form.cleaned_data['senha']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bem vindo(a), {username.title()}!')
                return redirect('index')

        context = {'form': form}
        messages.error(request, f'Nome de usuário/senha inválidos')

        return render(request, 'usuarios/login.html', context)


def sign_out(request):
    logout(request)
    messages.success(request,f'Logout efetuado.')

    return redirect('login')