from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Historico_Edicao
from contratos.models import Contratos
from obras.models import Obras
from diarios.models import Diarios

# Create your views here.
#views que lidam com historico de edições
@login_required
def historico_edicoes(request, tipo, id):
    historico = Historico_Edicao.objects.filter(tipo=tipo, tipo_id = id).order_by('-timestamp')
    if tipo == 'contrato':
        objeto = get_object_or_404(Contratos, id=id)

    if tipo == 'obra':
        objeto = get_object_or_404(Obras, id=id)

    if tipo == 'diario':
        objeto = get_object_or_404(Diarios, id=id)
    
    #implementar if de notificações

    return render(request, 'historico_edicoes.html', {'historico':historico, 'tipo':tipo, 'tipo_id':id, 'objeto':objeto})