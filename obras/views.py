
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#importação de models usados 
from utils.models import Historico_Edicao
from contratos.models import Contratos
from obras.models import Obras
from diarios.models import Diarios
#importação de formulários
from .forms import formCadastraObra, formEditaObra

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


    return render(request, 'controle_obras.html', {'contratos':contratos, 'obras':obras})

@login_required
def cadastra_obra(request, contrato_id):
    '''
    Gera e processa o formulário de cadastrar obra
    '''
    if request.method == 'GET':
        if contrato_id > 0:
            contrato = get_object_or_404(Contratos, id=contrato_id)
        else:
            contrato = None

        form = formCadastraObra(initial = {'contrato':contrato})
    
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
            
    
    return render(request, 'cadastra_obra.html', {'form':form})

@login_required
def visualiza_obra(request, id):
    '''
    Retorna a obra, seu histórico de edições e os diários e notificações ligadas a ela.
    '''
    #dados da obra
    obra = get_object_or_404(Obras, id=id)
    #dados de edições
    historico_edicoes = Historico_Edicao.objects.filter(tipo='obra', tipo_id=obra.id).order_by('-timestamp')
    #dados de diários
    diarios = Diarios.objects.filter(obra=obra)
    
    #implementar notificações quando disponível

    return render(request, 'visualiza_obra.html', {'obra':obra, 'diarios':diarios, 'historico':historico_edicoes})

@login_required
def edita_obra(request, id):
    '''
    Responsável pela criação do formulário e processamento da edição de obras
    '''
    obra = get_object_or_404(Obras, id=id)
    #Caso o request seja GET monta o formulário com os dados cadastrados
    if request.method == 'GET':
        form = formEditaObra(instance=obra)

    #Caso o request seja POT valida o formulário, procura por alterações para registro
    #e atualiza os novos dados
    if request.method == 'POST':
        form = formEditaObra(request.POST, instance=obra)
        
        nome_antigo = obra.nome
        local_antigo = obra.local
        inicio_antigo = obra.inicio
        termino_antigo = obra.termino
        situacao_antiga = obra.situacao
        contrato_antigo = obra.contrato
        empresa_antiga = obra.empresa_responsavel

        if form.is_valid():

            #Descobre qual campo foi alterado e gera a mensagem de alteração para o histórico
            alteracoes = {}
            
            if nome_antigo != form.cleaned_data['nome']:
                alteracoes['nome'] = f"Foi alterado o campo Nome. De {obra.nome} para {form.cleaned_data['nome']}."
            if local_antigo != form.cleaned_data['local']:
                alteracoes['local'] = f"Foi alterado o campo Local. De {obra.local} para {form.cleaned_data['local']}."
            novo_inicio = form.cleaned_data['inicio']
            if inicio_antigo != novo_inicio and novo_inicio:
                alteracoes['inicio'] = f"Foi alterado o campo Data de Início. De {obra.inicio.strftime('%d/%m/%Y')} para {novo_inicio.strftime('%d/%m/%Y')}."
            novo_termino = form.cleaned_data['termino']
            if termino_antigo != novo_termino and novo_termino:
                alteracoes['termino'] = f"Foi alterado o campo Previsão de Término. De {obra.termino.strftime('%d/%m/%Y')} para {novo_termino.strftime('%d/%m/%Y')}."
            nova_situacao = form.cleaned_data['situacao']
            if situacao_antiga != nova_situacao:
                alteracoes['situacao'] = f"Foi alterado o campo Situação. De {obra.get_situacao_display()} para {dict(Obras.SITUACAO_CHOICES)[nova_situacao]}."
            if contrato_antigo != form.cleaned_data['contrato']:
                alteracoes['contrato'] = f"Foi alterado o campo Contrato. De {obra.contrato} para {form.cleaned_data['contrato']}."
            if empresa_antiga != form.cleaned_data['empresa_responsavel']:
                alteracoes['empresa_responsavel'] = f"Foi alterado o campo Empresa Responsável. De {obra.empresa_responsavel} para {form.cleaned_data['empresa_responsavel']}."
            
             #Caso alteracoes tenha algum registro, itera sobre eles e salva todos em 'Historico_Edicao'
            if len(alteracoes.items()) > 0:
                alteracoes_texto = " | ".join(alteracoes.values())
                for campo, descricao in alteracoes.items():
                    Historico_Edicao.objects.create(
                        tipo = 'obra',
                        tipo_id = obra.id,
                        descricao_alteracao = descricao,
                        usuario = request.user
                    )
            
                #Gera mensagens de sucessos para cada alteração realizada
                messages.add_message(
                                        request,
                                        messages.SUCCESS,
                                        f"{obra} foi alterada com sucesso. Alterações: {alteracoes_texto}"
                                        )

                #Substitui os dados para salvar a edição
                # obra.nome = form.cleaned_data['nome']
                # obra.local = form.cleaned_data['local']
                # obra.inicio = form.cleaned_data['inicio']
                # obra.termino = form.cleaned_data['termino']
                # obra.contrato = form.cleaned_data['contrato']
                # obra.empresa_responsavel = form.cleaned_data['empresa_responsavel']
                form.save()

                return redirect("controle_obras")
        
            else:
                messages.add_message(request, messages.constants.WARNING, f"Não foram detectadas alterações.")
        else:
            pass
    
    return render(request, 'edita_obra.html', {'form':form, 'obra':obra})

@login_required
def exclui_obra(request, id):
    diarios = Diarios.objects.filter(obra=id).select_related("obra")
    if diarios:
        messages.add_message(request,
                             messages.ERROR,
                             f"Não é possível excluir a obra {diarios[0].obra}. Ela já possui diários vinculados a ela. Ainda é possível desativá-la para que não apareça para emissão de diários e notificações.")
        return redirect('visualiza_obra', id=id)
    else:
        obra = get_object_or_404(Obras, id=id)
        nome_obra = obra.nome
        obra.delete()
        messages.add_message(request,
                             messages.SUCCESS,
                             f"A obra {nome_obra} foi excluída com sucesso.")
        return redirect('controle_obras')
    
