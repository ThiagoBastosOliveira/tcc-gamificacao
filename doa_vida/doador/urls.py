from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('usuarios/', views.user, name='user'),
    path('indicadores/', views.indicadores, name='dashboard'),
    path('register-user/', views.cadastro_user, name='cadastro-user')
]