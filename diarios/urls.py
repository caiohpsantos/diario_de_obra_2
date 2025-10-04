from django.urls import path
from . import views

urlpatterns = [
    path('', views.controle_contratos),
    #rotas que lidam com os contratos
    path('controle_contratos/', views.controle_contratos, name='controle_contratos'),
    path('cadastra_contrato/', views.cadastra_contrato, name='cadastra_contrato'),
    path('visualiza_contrato/<int:id>/', views.visualiza_contrato, name='visualiza_contrato'),
    path('edita_contrato/<int:id>/', views.edita_contrato, name='edita_contrato'),
    path('exclui_contrato/<int:id>/', views.exclui_contrato, name='exclui_contrato'),
    #rotas que lidam com as obras
    path('controle_obras/', views.controle_obras, name='controle_obras'),
    path('cadastra_obra/', views.cadastra_obra, name='cadastra_obra'),
    path('visualiza_obra/<int:id>/', views.visualiza_obra, name='visualiza_obra'),
    path('edita_obra/<int:id>/', views.edita_obra, name='edita_obra'),
    path('exclui_obra/<int:id>/', views.exclui_obra, name='exclui_obra'),
    #rotas que lidam com serviços padrão
    path('controle_servicos_padrao/', views.controle_servicos_padrao, name='controle_servicos_padrao'),
    path('edita_servicos_padrao_ajax/', views.edita_servicos_padrao_ajax, name='edita_servicos_padrao_ajax'),
    path('exclui_servicos_padrao/<int:id>/', views.exclui_servicos_padrao, name='exclui_servicos_padrao'),
    #path('controle_diarios/', views.controle_diarios, name='controle_diarios'),
    #rota para visualização das edições gravadas para determinado registro
    path('historico_edicoes/<str:tipo>/<int:id>/', views.historico_edicoes, name='historico_edicoes')
    

]