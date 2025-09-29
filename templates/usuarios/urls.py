from django.urls import path
from . import views, forms
from django.contrib.auth import views as authviews   

urlpatterns = [
    #links de login,logout e gerenciamento da conta
    path('login/', authviews.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', views.deslogar, name="logout"),
    path('controle_conta/', views.controle_de_conta, name="controle_conta"),
    path('atualiza_dados_usuario/', views.atualiza_dados_usuario, name='atualiza_dados_usuario'),
    path('atualiza_endereco_usuario/', views.atualiza_endereco_usuario, name='atualiza_endereco_usuario'),
    #links para troca de senha
    path('password_reset/', authviews.PasswordResetView.as_view(template_name='usuarios/troca_senha.html'),name='password_reset'),
    path('password_reset/done/', authviews.PasswordResetDoneView.as_view(template_name='usuarios/troca_senha_enviada.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', authviews.PasswordResetConfirmView.as_view(template_name='usuarios/troca_senha_confirmacao.html'), name='password_reset_confirm'),
    path('reset/done/', authviews.PasswordResetCompleteView.as_view(template_name='usuarios/troca_senha_completa.html'), name='password_reset_complete'),
    #link para criar novos usuários (só administradores)
    path('cria_novo_usuario/', views.cria_novo_usuario, name='cria_novo_usuario')
]
