from django.shortcuts import render
from .models import Estoque, Doador, Badge, Hemocentro


def index(request):

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
    doador = Doador.objects.get(id=1)
    badges = Badge.objects.all()
    doadores = Doador.objects.all()
    doadores = sorted(doadores, key=lambda t: t.calcular_pontuacao(), reverse=True)
    badges2 = []
    for badge in badges:
        if badge.doador_set.filter(id=1):
            valor = True
        else:
            valor = False
        badges2.append({'badge': badge, 'tem': valor})
    context = {'estoque': estoque, 'doador': doador, 'badges': badges2, 'doadores': doadores}

    return render(request, 'doador/index.html', context)


def user(request):

    doador = Doador.objects.get(id=1)
    context = {'doador': doador}

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
    doador = Doador.objects.get(id=1)

    context = {'estoque': estoque, 'unidade': unidade, 'doador': doador}

    return render(request, 'doador/indicadores.html', context)
