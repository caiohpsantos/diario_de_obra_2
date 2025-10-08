from django.urls import path
from . import views

urlpatterns = [
    path('', views.controle_contratos),
    #rotas que lidam com os contratos
    path('controle_contratos/', views.controle_contratos, name='controle_contratos'),
    path('cadastra_contrato/', views.cadastra_contrato, name='cadastra_contrato'),
    path('visualiza_contrato/<int:id>/', views.visualiza_contrato, name='visualiza_contrato'),
    path('edita_contrato/<int:id>/', views.edita_contrato, name='edita_contrato'),
    path('exclui_contrato/<int:id>/', views.exclui_contrato, name='exclui_contrato')

]