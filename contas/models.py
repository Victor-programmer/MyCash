from django.db import models
from enum import Enum

class Bancos(models.TextChoices):
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    BRADESCO = 'Bradesco'
    ITAU = 'Itaú'
    INTER = 'Inter'
    DINHEIRO = 'Dinheiro'

class Status(models.TextChoices):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

class Tipos(models.TextChoices):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

class Conta(models.Model):
    banco = models.CharField(max_length=20, choices=Bancos.choices, default=Bancos.NUBANK)
    valor = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVO)

from django.db import models
from datetime import datetime

class Tipos(models.TextChoices):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

class Historico(models.Model):
    conta = models.ForeignKey('Conta', on_delete=models.CASCADE)  # Associa a conta
    tipo = models.CharField(max_length=10, choices=Tipos.choices, default=Tipos.ENTRADA)
    motivo = models.CharField(max_length=255)
    valor = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)  # Salva a data automaticamente
