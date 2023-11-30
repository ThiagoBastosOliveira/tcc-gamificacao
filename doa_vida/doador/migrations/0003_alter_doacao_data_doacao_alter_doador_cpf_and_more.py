# Generated by Django 4.1 on 2023-11-30 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doador', '0002_hemocentro_alter_doacao_data_doacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doacao',
            name='data_doacao',
            field=models.DateField(default=datetime.date(2023, 11, 29)),
        ),
        migrations.AlterField(
            model_name='doador',
            name='cpf',
            field=models.CharField(max_length=14, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='doador',
            name='telefone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='estoque',
            name='data',
            field=models.DateField(default=datetime.date(2023, 11, 29)),
        ),
    ]