from django.urls import path
from . import views

urlpatterns = [
    
    #rotas que lidam com serviços padrão
    path('controle_servicos_padrao/', views.controle_servicos_padrao, name='controle_servicos_padrao'),
    path('edita_servicos_padrao_ajax/', views.edita_servicos_padrao_ajax, name='edita_servicos_padrao_ajax'),
    path('exclui_servicos_padrao/<int:id>/', views.exclui_servicos_padrao, name='exclui_servicos_padrao'),
    #path('controle_diarios/', views.controle_diarios, name='controle_diarios'),
   
    

]