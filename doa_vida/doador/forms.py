from django import forms
from doador.models import Doador


class CadastroForm(forms.ModelForm):
    class Meta:
        model = Doador
        fields = ['cpf', 'cns', 'nome', 'num_ident', 'nome', 'sexo', 'nome_pai', 'nome_mae',
                  'grupo_abo', 'fator_rh', 'telefone', 'estado']
