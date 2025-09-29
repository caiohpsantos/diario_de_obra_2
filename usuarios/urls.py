from django.urls import path
from django.contrib.auth import views as authviews
from . import views

urlpatterns = [
    #links login, logout e gerenciamento de conta
    path('login/', authviews.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', views.deslogar, name="logout"),
    path('novo_usuario/', views.criar_usuario, name="novo_usuario"),
    path('alterar_dados_usuario', views.alterar_dados_usuario, name='alterar_dados_usuario'),
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    # links para troca de senha
   #links para troca de senha
    path('password_reset/', authviews.PasswordResetView.as_view(template_name='usuarios/troca_senha.html'),name='password_reset'),
    path('password_reset/done/', authviews.PasswordResetDoneView.as_view(template_name='usuarios/troca_senha_enviada.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', authviews.PasswordResetConfirmView.as_view(template_name='usuarios/troca_senha_confirmacao.html'), name='password_reset_confirm'),
    path('reset/done/', authviews.PasswordResetCompleteView.as_view(template_name='usuarios/troca_senha_completa.html'), name='password_reset_complete'),
]   