from django.urls import path
from . import views

urlpatterns = [
    
    #rotas que lidam com as obras
    path('controle_obras/', views.controle_obras, name='controle_obras'),
    path('cadastra_obra/<int:contrato_id>/', views.cadastra_obra, name='cadastra_obra'),
    path('visualiza_obra/<int:id>/', views.visualiza_obra, name='visualiza_obra'),
    path('edita_obra/<int:id>/', views.edita_obra, name='edita_obra'),
    path('exclui_obra/<int:id>/', views.exclui_obra, name='exclui_obra')
]