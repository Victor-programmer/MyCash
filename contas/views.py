from django.shortcuts import render, redirect, get_object_or_404
from .services import criar_conta, listar_contas, desativar_conta, transferir_saldo, movimentar_dinheiro, total_contas
from .models import Conta, Bancos, Status, Tipos

def index(request):
    contas = listar_contas()
    total = total_contas()
    return render(request, 'contas/index.html', {'contas': contas, 'total_contas': total})

from django.shortcuts import render, redirect
from .models import Bancos, Conta

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Conta

def criar_conta_view(request):
    if request.method == 'POST':
        banco = request.POST.get('banco')
        valor = float(request.POST.get('valor'))

        # Verifica se a conta já existe
        conta_existente = Conta.objects.filter(banco=banco).first()

        if conta_existente:
            messages.error(request, 'Essa conta já existe.')
        else:
            # Cria a conta caso não exista
            Conta.objects.create(banco=banco, valor=valor, status="Ativo")
            messages.success(request, 'Conta criada com sucesso.')

        return redirect('index')  # Redireciona para a página principal

    # Passa os bancos para o template
    bancos = Bancos
    return render(request, 'contas/criar_conta.html', {'bancos': bancos})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Conta

def desativar_conta_view(request, id):
    conta = get_object_or_404(Conta, id=id)

    if conta.valor > 0:
        messages.error(request, 'Essa conta ainda possui saldo e não pode ser desativada.')
    else:
        # Define como inativo antes de excluir
        conta.status = 'Inativo'
        conta.save()
        
        # Remove a conta do banco de dados
        conta.delete()
        
        messages.success(request, 'Conta desativada e removida com sucesso.')

    return redirect('index')  # Redireciona para a página principal


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Conta

def transferir_saldo_view(request):
    if request.method == 'POST':
        conta_saida_id = int(request.POST.get('conta_saida'))
        conta_entrada_id = int(request.POST.get('conta_entrada'))
        valor = float(request.POST.get('valor'))
        motivo = request.POST.get('motivo')

        # Obtém as contas do banco de dados
        conta_saida = get_object_or_404(Conta, id=conta_saida_id)
        conta_entrada = get_object_or_404(Conta, id=conta_entrada_id)

        # Verifica se há saldo suficiente
        if conta_saida.valor < valor:
            messages.error(request, 'Saldo insuficiente para realizar a transferência.')
        else:
            # Realiza a transferência
            conta_saida.valor -= valor
            conta_entrada.valor += valor
            conta_saida.save()
            conta_entrada.save()
            messages.success(request, 'Transferência realizada com sucesso.')

    return redirect('index')  # Redireciona para a página principal


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Conta

def movimentar_dinheiro_view(request):
    if request.method == 'POST':
        conta_id = int(request.POST.get('conta_id'))
        tipo = request.POST.get('tipo')
        valor = float(request.POST.get('valor'))
        motivo = request.POST.get('motivo')

        # Obtém a conta do banco de dados
        conta = get_object_or_404(Conta, id=conta_id)

        # Verifica se a movimentação é uma saída e se há saldo suficiente
        if tipo == "SAIDA" and conta.valor < valor:
            messages.error(request, 'Saldo insuficiente para realizar esta movimentação.')
        else:
            # Realiza a movimentação
            if tipo == "SAIDA":
                conta.valor -= valor
            else:  # Se for "ENTRADA"
                conta.valor += valor
            
            conta.save()
            messages.success(request, 'Movimentação realizada com sucesso.')

    return redirect('index')  # Redireciona para a página principal



import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.shortcuts import render
from .models import Conta

def criar_grafico_por_conta():
    contas = Conta.objects.filter(status="Ativo")  # Filtra contas ativas
    bancos = [conta.banco for conta in contas]
    total = [conta.valor for conta in contas]

    # Criar o gráfico
    fig, ax = plt.subplots()
    ax.bar(bancos, total, color='#28a745')
    ax.set_xlabel('Banco')
    ax.set_ylabel('Saldo')
    ax.set_title('Saldo por Banco')

    # Converter o gráfico em uma imagem base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.getvalue()).decode()
    uri = "data:image/png;base64," + string
    return uri

def index(request):
    contas = Conta.objects.all()
    total_contas = sum(conta.valor for conta in contas)
    
    # Gerar gráfico
    grafico = criar_grafico_por_conta()

    return render(request, 'contas/index.html', {
        'contas': contas,
        'total_contas': total_contas,
        'grafico': grafico
    })
from django.shortcuts import render
from .models import Historico
from datetime import datetime, timedelta

def buscar_historico_entre_datas(data_inicio, data_fim):
    """ Filtra transações entre datas específicas """
    return Historico.objects.filter(data__range=[data_inicio, data_fim])

def historico_view(request):
    historico = Historico.objects.none()  # QuerySet vazio inicialmente

    if request.method == "POST":
        data_inicio = request.POST.get("data_inicio")
        data_fim = request.POST.get("data_fim")

        if data_inicio and data_fim:
            try:
                # Converte as datas de string para formato correto
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

                # Adiciona um dia à data_fim para incluir transações no próprio dia
                data_fim += timedelta(days=1)

                # Chama a função de filtragem
                historico = buscar_historico_entre_datas(data_inicio, data_fim)
            except ValueError:
                # Caso haja erro na conversão, mantém o QuerySet vazio
                pass

    return render(request, "contas/historico.html", {"historico": historico})