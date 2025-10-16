from django.urls import path
from . import views

urlpatterns = [
    
    #rotas que lidam com serviços padrão
    path('controle_servicos_padrao/', views.controle_servicos_padrao, name='controle_servicos_padrao'),
    path('edita_servicos_padrao_ajax/', views.edita_servicos_padrao_ajax, name='edita_servicos_padrao_ajax'),
    path('exclui_servicos_padrao/<int:id>/', views.exclui_servicos_padrao, name='exclui_servicos_padrao'),
    #rotas que lidam com efetivo direto padrão
    path('controle_efetivo_direto_padrao/', views.controle_efetivo_direto_padrao, name='controle_efetivo_direto_padrao'),
    path('edita_efetivo_direto_padrao_ajax/', views.edita_efetivo_direto_padrao_ajax, name="edita_efetivo_direto_padrao_ajax"),
    path('excluir_efetivo_direto_padrao/<int:id>/', views.exclui_efetivo_direto_padrao, name='excluir_efetivo_direto_padrao'),
    #rotas que lidam com efetivo INdireto padrão
    path('controle_efetivo_indireto_padrao/', views.controle_efetivo_indireto_padrao, name='controle_efetivo_indireto_padrao'),
    path('edita_efetivo_indireto_padrao_ajax/', views.edita_efetivo_indireto_padrao_ajax, name="edita_efetivo_indireto_padrao_ajax"),
   
    #path('controle_diarios/', views.controle_diarios, name='controle_diarios'),
   
    

]