from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import numpy as np


class Badge(models.Model):
    nome = models.CharField(max_length=100)
    regra = models.CharField(max_length=100)
    imagem = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('regra').choices = [(member, member) for member in dir(self) if
                                                 member.startswith("regra_")]

    def __str__(self):
        return self.nome

    def regra_mais_100_pontos(self, doador):
        if doador.calcular_pontuacao() >= 100:
            return True
        else:
            return False

    def regra_mais_500_pontos(self, doador):
        if doador.calcular_pontuacao() >= 500:
            return True
        else:
            return False

    def verificar_regra(self, doador):
        return eval("self." + self.regra + "(doador)")


class Doador(models.Model):
    id_hemovida = models.CharField("Identificador no sistema Hemovida", max_length=9)
    cpf = models.CharField("CPF", max_length=11)
    cns = models.CharField("Número do Cartão Nacional de Saúde", max_length=30, null=True, blank=True)
    num_ident = models.CharField("Número da Identidade", max_length=11)
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    data_nascimento = models.DateField(default='1900-01-01')
    nome_pai = models.CharField("Nome do Pai", max_length=100, null=True, blank=True)
    nome_mae = models.CharField("Nome da Mãe", max_length=100)
    grupo_abo = models.CharField("Grupo ABO", max_length=2, choices=[('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB')])
    fator_rh = models.CharField("Fator RH", max_length=1, choices=[('+', '+'), ('-', '-')])
    telefone = models.CharField(max_length=11)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return self.nome

    def calcular_vidas_salvas(self):
        VIDAS_POR_DOACAO = 5  # TODO: Implementar cálculo de vidas salvas

        quantidade_doacoes = self.doacao_set.count()
        return quantidade_doacoes * VIDAS_POR_DOACAO

    def obter_ultima_doacao(self):
        try:
            ultima_doacao = self.doacao_set.latest('data_doacao')
            return ultima_doacao
        except Doacao.DoesNotExist:
            return None

    def obter_proxima_doacao(self):
        ultima_doacao = self.obter_ultima_doacao()
        if ultima_doacao:
            return ultima_doacao.data_doacao + datetime.timedelta(days=ultima_doacao.dias_inapto)
        else:
            return datetime.date.today()

    def obter_dias_proxima_doacao(self):
        proxima_doacao = self.obter_proxima_doacao()
        return (proxima_doacao - datetime.date.today()).days

    def calcular_pontuacao(self):
        try:
            doacoes = self.doacao_set.all()
            pontos = 0
            for doacao in doacoes:
                pontos += round(abs(np.log10((datetime.date.today() - doacao.data_doacao).days / 365)) * 100)
        except Doacao.DoesNotExist:
            pontos = 0

        return pontos

    def obter_historico_pontos(self):
        try:
            historico = {'datas': [], 'pontos': []}
            doacoes = self.doacao_set.all().order_by('data_doacao')
            pontuacao_acumulada = 0
            for doacao in doacoes:
                pontuacao_acumulada += round(
                    abs(np.log10((datetime.date.today() - doacao.data_doacao).days / 365)) * 100)
                historico['datas'].append(doacao.data_doacao.strftime('%Y-%m-%d'))  # TODO Implementar cálculo de pontos
                historico['pontos'].append(pontuacao_acumulada)
        except Doacao.DoesNotExist:
            historico = {}

        return historico


class Doacao(models.Model):
    doador = models.ForeignKey(Doador, on_delete=models.CASCADE)
    data_doacao = models.DateField(default=datetime.date.today())
    dias_inapto = models.IntegerField(default=60)  # TODO: Implementar cálculo de inaptidão

    def __str__(self):
        return "{} - {}".format(self.data_doacao.strftime("%d/%m/%Y"), self.doador.nome)


class Estoque(models.Model):
    grupo_abo = models.CharField("Grupo ABO", max_length=2, choices=[('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB')])
    fator_rh = models.CharField("Fator RH", max_length=1, choices=[('+', '+'), ('-', '-')])
    data = models.DateField(default=datetime.date.today())
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.grupo_abo + self.fator_rh + " | " + self.data.strftime("%d/%m/%Y") + " | " + str(self.quantidade)

    def obter_estado(self):
        if self.quantidade < 10:
            return "Crítico"
        elif self.quantidade < 50:
            return "Alerta"
        else:
            return "Estável"


class Hemocentro(models.Model):
    cnes_hemocentro = models.CharField("Cadastro Nacional de Estabelecimento de Saúde", max_length=9)
    nome = models.CharField(choices=[('HEMOGO - Goiânia', 'HEMOGO - Goiânia'), ('HEMOGO Ceres', 'HEMOGO Ceres'),
                                     ('HEMOGO - Catalão', 'HEMOGO - Catalão'),
                                     ('HEMOGO - Rio Verde', 'HEMOGO - Rio Verde'),
                                     ('HEMOGO - Jataí', 'HEMOGO - Jataí'), ('UCT - Formosa', 'UCT - Formosa'),
                                     ('UCT - Iporá', 'UCT - Iporá'), ('UCT - Porangatu', 'UCT - Porangatu'),
                                     ('UCT - Quirinópolis', 'UCT-Quirinópolis')], max_length=100),
    cod_ibge = models.CharField(max_length=7),
    municipio = models.CharField(choices=[('Goiânia', 'Goiânia'), ('Ceres', 'Ceres'), ('Catalão', 'Catalão'),
                                          ('Rio Verde', 'Rio Verde'), ('Jataí', 'Jataí'), ('Formosa', 'Formosa'),
                                          ('Iporá', 'Iporá'), ('Porangatu', 'Porangatu'),
                                          ('Quirinópolis', 'Quirinópolis')],
                                 max_length=20)

    def __str__(self):
        return self.nome


@receiver(post_save, sender=Doacao)
@receiver(post_delete, sender=Doacao)
def atualizar_badges(sender, instance, **kwargs):
    for badge in Badge.objects.all():
        if badge.verificar_regra(instance.doador):
            instance.doador.badges.add(badge)
        else:
            instance.doador.badges.remove(badge)

#  Indicações, desafios
