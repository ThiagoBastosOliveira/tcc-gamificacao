from django.shortcuts import render, redirect
from .forms import CadastroForm
from .models import Estoque, Doador, Badge, Hemocentro


def home(request):
    estoque = {
        'amais': Estoque.objects.filter(grupo_abo='A', fator_rh='+').order_by('-data')[0],
        'amenos': Estoque.objects.filter(grupo_abo='A', fator_rh='-').order_by('-data')[0],
        'abmais': Estoque.objects.filter(grupo_abo='AB', fator_rh='+').order_by('-data')[0],
        'abmenos': Estoque.objects.filter(grupo_abo='AB', fator_rh='-').order_by('-data')[0],
        'bmais': Estoque.objects.filter(grupo_abo='B', fator_rh='+').order_by('-data')[0],
        'bmenos': Estoque.objects.filter(grupo_abo='B', fator_rh='-').order_by('-data')[0],
        'omais': Estoque.objects.filter(grupo_abo='O', fator_rh='+').order_by('-data')[0],
        'omenos': Estoque.objects.filter(grupo_abo='O', fator_rh='-').order_by('-data')[0],
    }
    id_usuario = request.user.id
    doador = Doador.objects.get(id=id_usuario)
    badges = Badge.objects.all()
    doadores = Doador.objects.all()
    doadores = sorted(doadores, key=lambda t: t.calcular_pontuacao(), reverse=True)
    badges2 = []
    for badge in badges:
        if badge.doador_set.filter(id=id_usuario):

            valor = True
        else:
            valor = False
        badges2.append({'badge': badge, 'tem': valor})
    context = {'estoque': estoque, 'doador': doador, 'badges': badges2, 'doadores': doadores}

    return render(request, 'doador/home.html', context)


def user(request):
    id_usuario = request.user.id
    doador = Doador.objects.get(id=id_usuario)
    doadores = Doador.objects.all()
    doadores = sorted(doadores, key=lambda t: t.calcular_pontuacao(), reverse=True)
    badges = Badge.objects.all()
    badges2 = []
    for badge in badges:
        if badge.doador_set.filter(id=id_usuario):
            valor = True
        else:
            valor = False
        badges2.append({'badge': badge, 'tem': valor})

    context = {'doador': doador, 'badges': badges2, 'doadores': doadores}

    return render(request, 'doador/user.html', context)


def indicadores(request):
    estoque = {
        'amais': Estoque.objects.filter(grupo_abo='A', fator_rh='+').order_by('-data')[0],
        'amenos': Estoque.objects.filter(grupo_abo='A', fator_rh='-').order_by('-data')[0],
        'abmais': Estoque.objects.filter(grupo_abo='AB', fator_rh='+').order_by('-data')[0],
        'abmenos': Estoque.objects.filter(grupo_abo='AB', fator_rh='-').order_by('-data')[0],
        'bmais': Estoque.objects.filter(grupo_abo='B', fator_rh='+').order_by('-data')[0],
        'bmenos': Estoque.objects.filter(grupo_abo='B', fator_rh='-').order_by('-data')[0],
        'omais': Estoque.objects.filter(grupo_abo='O', fator_rh='+').order_by('-data')[0],
        'omenos': Estoque.objects.filter(grupo_abo='O', fator_rh='-').order_by('-data')[0],
    }
    unidade = Hemocentro.objects.all()
    id_usuario = request.user.id
    doador = Doador.objects.get(id=id_usuario)

    context = {'estoque': estoque, 'unidade': unidade, 'doador': doador}

    return render(request, 'doador/indicadores.html', context)


def cadastro_user(request):

    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, 'doador/dados_usuarios.html', {'form': form})

    else:
        form = CadastroForm()

    return render(request, 'doador/dados_usuarios.html', {'form': form})


def index(request):
    return render(request, 'doador/index.html', context=dict())
