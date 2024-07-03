from django.contrib import admin
from .models import Usuario, Doacao, Badge, Estoque, Hemocentro

admin.site.register(Usuario)
admin.site.register(Doacao)
admin.site.register(Badge)
admin.site.register(Estoque)
admin.site.register(Hemocentro)