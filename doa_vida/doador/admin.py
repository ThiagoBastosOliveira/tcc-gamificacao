from django.contrib import admin
from .models import Doador, Doacao, Badge, Estoque

admin.site.register(Doador)
admin.site.register(Doacao)
admin.site.register(Badge)
admin.site.register(Estoque)