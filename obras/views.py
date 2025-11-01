
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry
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
        contrato = get_object_or_404(Contratos, id=contrato_id) if contrato_id and contrato_id > 0 else None
        form = formCadastraObra(initial={'contrato': contrato})

    elif request.method == 'POST':
        form = formCadastraObra(request.POST)
        if form.is_valid():
            try:
                # form.clean_area já retorna GEOSGeometry ou None
                obra = form.save(commit=False)
                area_geom = form.cleaned_data.get("area")
                if area_geom is not None:
                    # se por algum acaso retornou string (defensivo), converte:
                    if isinstance(area_geom, str):
                        area_geom = GEOSGeometry(area_geom)
                    # garante SRID 4326
                    if getattr(area_geom, "srid", None) is None:
                        area_geom.srid = 4326
                    elif area_geom.srid != 4326:
                        area_geom.transform(4326)
                    obra.area = area_geom
                else:
                    obra.area = None

                obra.save()

                # registro historico
                Historico_Edicao.objects.create(
                    tipo="obra",
                    tipo_id=obra.id,
                    descricao_alteracao="Criação do registro",
                    usuario=request.user
                )

                messages.success(request, f"{obra} cadastrada com sucesso!")
                return redirect('controle_obras')
            except Exception as e:
                # registramos o erro e deixamos o form reexibir com mensagens
                messages.error(request, f"Erro ao salvar obra: {e}")
                import traceback; traceback.print_exc()
        else:
            # form inválido: irá mostrar erros no template
            messages.error(request, "Formulário inválido. Verifique os campos destacados.")

    return render(request, 'cadastra_obra.html', {'form': form})

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
    obra = get_object_or_404(Obras, id=id)

    if request.method == "GET":
        form = formEditaObra(instance=obra)

    elif request.method == "POST":
        form = formEditaObra(request.POST, instance=obra)

        # Campos antigos para histórico
        campos_antigos = {
            "nome": obra.nome,
            "local": obra.local,
            "inicio": obra.inicio,
            "termino": obra.termino,
            "situacao": obra.situacao,
            "contrato": obra.contrato,
            "empresa_responsavel": obra.empresa_responsavel,
            "area": obra.area,
        }

        if form.is_valid():
            alteracoes = {}
            for campo, valor_antigo in campos_antigos.items():
                novo_valor = form.cleaned_data.get(campo)
                if campo in ["inicio", "termino"]:
                    if valor_antigo != novo_valor and novo_valor:
                        alteracoes[campo] = f"Campo {campo} alterado de {valor_antigo.strftime('%d/%m/%Y') if valor_antigo else 'vazio'} para {novo_valor.strftime('%d/%m/%Y')}."
                elif campo == "situacao":
                    if valor_antigo != novo_valor:
                        alteracoes[campo] = f"Campo Situação alterado de {dict(Obras.SITUACAO_CHOICES).get(valor_antigo)} para {dict(Obras.SITUACAO_CHOICES).get(novo_valor)}."
                elif campo == "area":
                    if valor_antigo != novo_valor:
                        alteracoes[campo] = "Campo Área da Obra alterado. Demarcações sofreram mudanças."
                else:
                    if valor_antigo != novo_valor:
                        alteracoes[campo] = f"Campo {campo} alterado de {valor_antigo} para {novo_valor}."

            form.save()

            if alteracoes:
                texto = " | ".join(alteracoes.values())
                for desc in alteracoes.values():
                    Historico_Edicao.objects.create(
                        tipo="obra",
                        tipo_id=obra.id,
                        descricao_alteracao=desc,
                        usuario=request.user,
                    )
                messages.success(request, f"{obra} atualizada com sucesso. Alterações: {texto}")
            else:
                messages.warning(request, "Não foram detectadas alterações.")

            return redirect("controle_obras")

    return render(request, "edita_obra.html", {"form": form, "obra": obra})


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
    
@login_required
def mapa_obra(request, id):
    """
    Exibe apenas o mapa da obra com a área.
    """
    obra = get_object_or_404(Obras, id=id)
    area_wkt = obra.area.wkt if obra.area else None

    context = {
        'obra': obra,
        'area_wkt': area_wkt
    }
    return render(request, 'mapa_obra.html', context)