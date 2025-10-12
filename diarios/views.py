import json
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Diarios, ServicosPadrao, Servicos, Efetivo_Direto_Padrao
from utils.models import Historico_Edicao



#views que lidam com servicos padrão
@login_required
def controle_servicos_padrao(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        if descricao:
            ServicosPadrao.objects.create(descricao=descricao)
            messages.add_message(request, messages.SUCCESS, f"Serviço {descricao} foi cadastrado com sucesso.")
        else:
            messages.add_message(request, messages.ERROR, f"Preencha o nome do serviço no campo de Descrição.")
        return redirect('controle_servicos_padrao')  # redireciona pra limpar o form

    servicos = ServicosPadrao.objects.all().order_by('descricao')
    return render(request, 'controle_servicos_padrao.html', {'servicos': servicos})

@login_required
@require_POST
def edita_servicos_padrao_ajax(request):
    try:
        data = json.loads(request.body)
        servico = ServicosPadrao.objects.get(id=data['id'])
        servico.descricao = data['descricao']
        servico.save()
        return JsonResponse({'sucesso': True})
    
    except ServicosPadrao.DoesNotExist:
        return JsonResponse({'sucesso': False, 'mensagem': 'Serviço não encontrado.'})
    
    except Exception as e:
        return JsonResponse({'sucesso': False, 'mensagem': str(e)})

@login_required    
def exclui_servicos_padrao(request, id):
    """
    Exclui um serviço padrão, desde que não esteja referenciado em nenhum diário.
    Caso esteja, exibe uma mensagem de erro informando que não é possível excluir.
    """
    servico_padrao = get_object_or_404(ServicosPadrao, id=id)
    existe_registro = Servicos.objects.filter(servicos_padrao_id = id).exists()
    if existe_registro:
        messages.add_message(request, messages.ERROR, f"Não é possível excluir o serviço {servico_padrao.descricao} pois ele já é referenciado em algum diário. Mas ainda pode editá-lo.")
    else:
        nome_servico = servico_padrao.descricao
        servico_padrao.delete()
        messages.add_message(request, messages.SUCCESS, f"O servico {nome_servico} foi excluído com sucesso.")
    return redirect("controle_servicos_padrao")

#views que lidam com efetivo direto
@login_required
def controle_efetivo_direto_padrao(request):
    if request.method == "POST":
        funcao = request.POST.get("funcao")
        qtde = request.POST.get("qtde")
        presente = request.POST.get("presente")

        if not funcao or not qtde or not presente:
            messages.add_message(request, messages.ERROR, "Os campos Função, Efetivo total e Efetivo presente não podem ser vazios.")
            redirect("controle_efetivo_direto_padrao")
        
        else:
            try:
                novo_efetivo = Efetivo_Direto_Padrao(funcao = funcao, qtde = int(qtde), presente = int(presente))
                novo_efetivo.save()
                messages.add_message(request, messages.SUCCESS, f"O novo efetivo {novo_efetivo.funcao} foi cadastrado com sucesso.")
            except Exception as e:
                messages.add_message(request, messages.ERROR, f"Houve um erro ao salvar o novo efetivo. Erro {e}")
        redirect("controle_efetivo_direto_padrao")

    efetivo_direto_padrao = Efetivo_Direto_Padrao.objects.all()
    return render(request, "controle_efetivo_direto_padrao.html", {"efetivos":efetivo_direto_padrao})

@login_required
@require_POST
def edita_efetivo_direto_padrao_ajax(request):
    try:
        data = json.loads(request.body)
        efetivo = Efetivo_Direto_Padrao.objects.get(id=data['id'])

        # Atualiza os campos
        efetivo.funcao = data.get('funcao', efetivo.funcao)
        qtde = int(data.get('qtde', efetivo.qtde))
        presente = int(data.get('presente', efetivo.presente))

        # Validação simples
        if qtde < 1:
            qtde = 1
        if presente < 1:
            presente = 1
        if presente > qtde:
            presente = qtde

        efetivo.qtde = qtde
        efetivo.presente = presente
        efetivo.save()

        return JsonResponse({'sucesso': True})
    
    except Efetivo_Direto_Padrao.DoesNotExist:
        return JsonResponse({'sucesso': False, 'mensagem': 'Efetivo não encontrado.'})
    except Exception as e:
        return JsonResponse({'sucesso': False, 'mensagem': str(e)})

@login_required    
def exclui_efetivo_direto_padrao(request, id):
    """
    Exclui um efetivo direto padrão.

    """
    try:
        efetivo_direto_padrao = get_object_or_404(Efetivo_Direto_Padrao, id=id)
        efetivo_funcao = efetivo_direto_padrao.funcao
        efetivo_direto_padrao.delete()
        messages.add_message(request, messages.SUCCESS, f"O efetivo {efetivo_funcao} foi excluído com sucesso.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, f"Não foi possível excluir o efetivo {efetivo_funcao}. Erro: {e}")
    
    return redirect("controle_efetivo_direto_padrao")