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
    
from django.db import models

class Historico(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=Tipos.choices)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255)
    data = models.DateField(auto_now_add=True)  # Usando DateField em vez de DateTimeField

    def __str__(self):
        return f"{self.tipo} - {self.valor} - {self.data}"
