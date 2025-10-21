
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contratos
from utils.models import Historico_Edicao
from .forms import formCadastraContrato, formEditaContrato
from obras.models import Obras
from diarios.models import Diarios


# Create your views here.


def status_ativo(status):
    '''
    #função que retorna o termo Ativo caso receba True e Inativo se receber False. Específica para o contrato
    '''
    return "Ativo" if status else "Inativo"

#views que lidam com contratos
@login_required
def controle_contratos(request):
    '''
    Função responsável por pesquisar todos os contratos e retornar para tela inicial de contratos
    '''
    if request.method == 'GET':
        contratos = Contratos.objects.all()
        contratos = Contratos.objects.annotate(qtd_obras=Count('obras'))
    else:
        messages.add_message(request, messages.constants.ERROR, "Este tipo de operação não é permitida. Esta rota só aceita o método GET.")
        return redirect('404.html')
    
    return render(request, "controle_contratos.html", { "contratos": contratos})

@login_required
def cadastra_contrato(request):
    '''
    Gera e processa o formulário pra cadastrar contrato.
    '''
    if request.method == "POST":
        form = formCadastraContrato(request.POST) 
        if form.is_valid(): 
            contrato = Contratos(**form.cleaned_data)
            contrato.save()
            #realiza o registro no Historico de Edições
            registro = Historico_Edicao(
                tipo="contrato",
                tipo_id=contrato.id,
                descricao_alteracao = f"Criação do registro",
                usuario = request.user
            )
            registro.save()
            messages.add_message(request, messages.constants.SUCCESS, f"Contrato {contrato} cadastrado com sucesso!")
            return redirect('controle_contratos')
    if request.method == "GET":
        form = formCadastraContrato()

    return render(request, "cadastra_contrato.html", {'form':form}) 

@login_required
def edita_contrato(request, id):
    '''
    Gera e processa o formulário de edição de contrato, validações estão no form formEditaContrato
    '''
    contrato = get_object_or_404(Contratos, id=id)
    
    #Caso o request seja GET monta o formulário com os dados cadastrados
    if request.method == "GET":
        form = formEditaContrato(initial={
            "numero": contrato.numero,
            "nome": contrato.nome,
            "cliente": contrato.cliente,
            "dia_inicia_relatorio": contrato.dia_inicia_relatorio,
            "dia_finaliza_relatorio": contrato.dia_finaliza_relatorio,
            "ativo": contrato.ativo
        })
    #Caso o request seja POST instancia o formulário com os dados recebidos
    else:
        form = formEditaContrato(request.POST, instance=contrato)
        #ao ser desmarcado, o campo ativo não vem no POST, por isso precisa capturar o valor antes de validar o form
        antigo_ativo = contrato.ativo
        if form.is_valid():
           
            #Descobre qual campo foi alterado e salva uma frase explicativa no dicionario 'alteracoes'
            alteracoes = {}
            if contrato.ativo != antigo_ativo:
                alteracoes['ativo'] = f'Foi alterado o campo "Ativo". De {status_ativo(contrato.ativo)} para {status_ativo(form.cleaned_data["ativo"])}.'
            if contrato.numero != form.cleaned_data['numero']:
                alteracoes['numero'] = f'Foi alterado o campo "Número". De "{contrato.numero}" para "{form.cleaned_data["numero"]}"'
            if contrato.nome != form.cleaned_data['nome']:
                alteracoes['nome'] = f'Foi alterado o campo "Nome". De "{contrato.nome}" para "{form.cleaned_data["nome"]}".'
            if contrato.cliente != form.cleaned_data['cliente']:
                alteracoes['cliente'] = f'Foi alterado o campo "Cliente". De "{contrato.cliente}" para "{form.cleaned_data["cliente"]}".'
            if contrato.dia_inicia_relatorio != form.cleaned_data['dia_inicia_relatorio']:
                alteracoes['inicial'] = f'Foi alterado o campo "Dia Inicial do Relatório". De "{contrato.dia_inicia_relatorio}" para "{form.cleaned_data["dia_inicia_relatorio"]}".'
            if contrato.dia_finaliza_relatorio != form.cleaned_data['dia_finaliza_relatorio']:
                alteracoes['finaliza'] = f'Foi alterado o campo "Dia que Finaliza o Relatório". De "{contrato.dia_finaliza_relatorio}" para "{form.cleaned_data["dia_finaliza_relatorio"]}".'
            
            #Caso alteracoes tenha algum registro, itera sobre eles e salva todos em 'Historico_Edicao'
            if len(alteracoes.items()) > 0:
                alteracoes_texto = " | ".join(alteracoes.values())
                for campo, descricao in alteracoes.items():
                    Historico_Edicao.objects.create(
                        tipo = 'contrato',
                        tipo_id = contrato.id,
                        descricao_alteracao = descricao,
                        usuario = request.user
                    )
                #Gera mensagens de sucessos para cada alteração realizada
                messages.add_message(
                                        request,
                                        messages.SUCCESS,
                                        f"Contrato {contrato} foi alterado com sucesso. Alterações: {alteracoes_texto}"
                                        )
            
                #Substitui os dados para salvar a edição
                contrato.ativo = form.cleaned_data['ativo']
                contrato.numero = form.cleaned_data['numero']
                contrato.nome = form.cleaned_data['nome']
                contrato.cliente = form.cleaned_data['cliente']
                contrato.dia_inicia_relatorio = form.cleaned_data['dia_inicia_relatorio']
                contrato.dia_finaliza_relatorio = form.cleaned_data['dia_finaliza_relatorio']
                contrato.save()
                
                return redirect("controle_contratos")
            else:
                 messages.add_message(request, messages.constants.WARNING, f"Não foram detectadas alterações.")
        else:
            pass
    return render(request, "edita_contrato.html", {"form": form, 'id':contrato.id})

@login_required
def visualiza_contrato(request, id):
    """
    Retorna o contrato, seu histórico de edições, obras, diários e notificações ligadas a ele.
    """
    #Dados do contrato
    contrato = get_object_or_404(Contratos, id=id)
    #Obras relacionadas
    obras = Obras.objects.filter(contrato=contrato).select_related("contrato")
    #Diarios relacionados
    diarios = Diarios.objects.filter(obra__contrato=contrato).select_related("obra__contrato")
    #Histórico de edição do contrato
    historico = Historico_Edicao.objects.filter(tipo='contrato', tipo_id=id).order_by('-timestamp')
    #Inserir pesquisa de notificações quando disponível
    return render(request, 'visualiza_contrato.html', {'contrato':contrato,'obras':obras, 'diarios':diarios, 'historico':historico})

@login_required
def exclui_contrato(request,id):
    obras = Obras.objects.filter(contrato=id).select_related("contrato")
    if obras:
        messages.add_message(request,
                             messages.ERROR,
                             f"Não é possível excluir o contrato {obras[0].contrato}. Ele já possui obras vinculadas a ele. Ainda é possível desativá-lo para que não apareça para emissão de diários e notificações.")
        return redirect('visualiza_contrato', id=id)
    else:
        contrato = get_object_or_404(Contratos, id=id)
        nome_contrato = contrato.nome
        contrato.delete()
        messages.add_message(request,
                             messages.SUCCESS,
                             f"O contrato {nome_contrato} foi excluído com sucesso.")
        return redirect('controle_contratos')

@login_required
def obras_por_contrato(request,id):
    obras = Obras.objects.filter(contrato_id=id, situacao="andamento").values("id", "nome")
    return JsonResponse(list(obras), safe=False)