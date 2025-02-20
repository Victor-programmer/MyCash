from django.shortcuts import get_object_or_404
from .models import Conta, Historico, Status, Tipos

def criar_conta(banco, valor):
    """
    Cria uma nova conta no banco de dados.
    """
    if Conta.objects.filter(banco=banco).exists():
        raise ValueError('Já existe uma conta nesse banco!')
    conta = Conta(banco=banco, valor=valor)
    conta.save()
    return conta

def listar_contas():
    """
    Retorna uma lista de todas as contas cadastradas.
    """
    return Conta.objects.all()

def desativar_conta(conta_id):
    """
    Desativa uma conta com base no ID.
    """
    conta = get_object_or_404(Conta, id=conta_id)
    if conta.valor > 0:
        raise ValueError('Essa conta ainda possui saldo e não pode ser desativada.')
    conta.status = Status.INATIVO
    conta.save()

def transferir_saldo(conta_saida_id, conta_entrada_id, valor, motivo):
    """
    Transfere saldo de uma conta para outra.
    """
    conta_saida = get_object_or_404(Conta, id=conta_saida_id)
    conta_entrada = get_object_or_404(Conta, id=conta_entrada_id)

    if conta_saida.valor < valor:
        raise ValueError('Saldo insuficiente na conta de saída.')

    conta_saida.valor -= valor
    conta_entrada.valor += valor

    # Registra a transferência no histórico
    from django.utils import timezone

    Historico.objects.create(
            conta=conta_saida,
        tipo=Tipos.SAIDA,
        valor=valor,
        motivo=f"Transferência para {conta_entrada.banco}: {motivo}",
        data=timezone.now()  # Defina a data manualmente
)
    Historico.objects.create(
        conta=conta_entrada,
        tipo=Tipos.ENTRADA,
        valor=valor,
        motivo=f"Transferência de {conta_saida.banco}: {motivo}",
        data=timezone.now()  # Defina a data manualmente
)

    conta_saida.save()
    conta_entrada.save()

def movimentar_dinheiro(conta_id, tipo, valor, motivo):
    """
    Realiza uma movimentação de dinheiro (entrada ou saída) em uma conta.
    """
    conta = get_object_or_404(Conta, id=conta_id)

    if tipo == Tipos.SAIDA and conta.valor < valor:
        raise ValueError('Saldo insuficiente para realizar a saída.')

    if tipo == Tipos.ENTRADA:
        conta.valor += valor
    else:
        conta.valor -= valor

    Historico.objects.create(
        conta=conta,
        tipo=tipo,
        valor=valor,
        motivo=motivo
    )

    conta.save()

def total_contas():
    """
    Calcula o total de saldo de todas as contas ativas.
    """
    contas_ativas = Conta.objects.filter(status=Status.ATIVO)
    return sum(conta.valor for conta in contas_ativas)

from django.utils import timezone

def buscar_historico_entre_datas(data_inicio, data_fim):
    """
    Retorna o histórico de movimentações entre duas datas.
    """
    return Historico.objects.filter(data__range=(data_inicio, data_fim))