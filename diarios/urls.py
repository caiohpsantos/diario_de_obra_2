from django.urls import path
from . import views

urlpatterns = [
    path('', views.controle_contratos),
    #rotas que lidam com os contratos
    path('controle_contratos/', views.controle_contratos, name='controle_contratos'),
    path('cadastra_contrato/', views.cadastra_contrato, name='cadastra_contrato'),
    path('visualiza_contrato/<int:id>/', views.visualiza_contrato, name='visualiza_contrato'),
    path('edita_contrato/<int:id>/', views.edita_contrato, name='edita_contrato'),
    #rotas que lidam com as obras
    path('controle_obras/', views.controle_obras, name='controle_obras'),
    path('cadastra_obra/', views.cadastra_obra, name='cadastra_obra'),
    path('edita_obra/<int:id>', views.edita_obra, name='edita_obra'),
    #rota para visualização das edições gravadas para determinado registro
    path('historico_edicoes/<str:tipo>/<int:id>', views.historico_edicoes, name='historico_edicoes')
    

]