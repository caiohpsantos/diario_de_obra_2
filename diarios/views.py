from django.shortcuts import render, redirect, HttpResponse
from .models import Contratos, Historico_Edicao, Obras, Diarios
from .forms import formCadastraContrato, formEditaContrato, formCadastraObra
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


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
    else:
        messages.add_message(request, messages.constants.ERROR, "Este tipo de operação não é permitida. Esta rota só aceita o método GET.")
        return redirect('404.html')
    
    return render(request, "contratos/controle_contratos.html", { "contratos": contratos})

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
            return redirect('contratos/controle_contratos')
    if request.method == "GET":
        form = formCadastraContrato()

    return render(request, "contratos/cadastra_contrato.html", {'form':form}) 

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
        form = formEditaContrato(request.POST)
        if form.is_valid():
           
            #Descobre qual campo foi alterado e salva uma frase explicativa no dicionario 'alteracoes'
            alteracoes = {}
            if contrato.ativo != form.cleaned_data['ativo']:
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
                
                return redirect("contratos/controle_contratos")
            else:
                 messages.add_message(request, messages.constants.WARNING, f"Não foram detectadas alterações.")
        else:
            pass
    return render(request, "contratos/edita_contrato.html", {"form": form, 'id':contrato.id})

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

    return render(request, 'contratos/visualiza_contrato.html', {'contrato':contrato,'obras':obras, 'darios':diarios, 'historico':historico})

#views que lidam com obras
@login_required
def controle_obras(request):
    '''
    Processa as buscas de obras, também popula o select de contratos no mesmo formulário
    '''
    
    #pesquisa contratos para popular o select de contratos
    contratos = Contratos.objects.all()

    #captura o que foi passado em cada campo    
    nome_obra = request.GET.get("nome_obra", "").strip()
    contrato_id = request.GET.get("contrato", "")
    situacao = request.GET.get("situacao", "")
    empresa = request.GET.get("empresa", "").strip()

    # Pesquisa mais importante, quanto ao contrato escolhido
    obras = Obras.objects.select_related("contrato").all()

    # Caso haja outras características, faz o filtro no que já foi pesquisado relativo ao contrato
    if nome_obra:
        obras = obras.filter(nome__icontains=nome_obra)
    if contrato_id:
        obras = obras.filter(contrato_id=contrato_id)
    if situacao:
        obras = obras.filter(situacao=situacao)
    if empresa:
        obras = obras.filter(empresa_responsavel__icontains=empresa)


    return render(request, 'obras/controle_obras.html', {'contratos':contratos, 'obras':obras})

def cadastra_obra(request):
    '''
    Gera e processa o formulário de cadastrar obra
    '''
    if request.method == 'GET':
        form = formCadastraObra()
    
    if request.method == 'POST':
        form = formCadastraObra(request.POST)
        if form.is_valid():
            obra = form.save()
             #realiza o registro no Historico de Edições
            registro = Historico_Edicao(
                tipo="obra",
                tipo_id=obra.id,
                descricao_alteracao = f"Criação do registro",
                usuario = request.user
            )
            registro.save()
            messages.add_message(request, messages.constants.SUCCESS, f"{obra} cadastrada com sucesso!")
            return redirect('controle_obras')
            
    
    return render(request, 'obras/cadastra_obra.html', {'form':form})
#views que lidam com historico de edições
@login_required
def historico_edicoes(request, tipo, id):
    historico = Historico_Edicao.objects.filter(tipo=tipo, tipo_id = id)

    return render(request, 'historico_edicoes.html', {'historico':historico})