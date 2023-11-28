from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.user, name='user'),
    path('indicadores/', views.indicadores, name='dashboard')
]