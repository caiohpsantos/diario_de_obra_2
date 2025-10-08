import json
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Diarios, ServicosPadrao, Servicos
from utils.models import Historico_Edicao



#views que lidam com diario
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

@require_POST
@csrf_exempt
def edita_servicos_padrao_ajax(request):
    try:
        data = json.loads(request.body)
        servico = ServicosPadrao.objects.get(id=data['id'])
        servico.descricao = data['descricao']
        servico.save()
        return JsonResponse({'sucesso': True})
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

