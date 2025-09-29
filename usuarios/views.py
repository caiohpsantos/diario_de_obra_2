from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import formCadastrarNovoUsuario, formAlterarDadosUsuario
import random
import string


@login_required
def pagina_inicial(request):
     consulta = get_object_or_404(User, username=request.user)
     if not consulta.last_login:
          return redirect('criar_primeira_senha')
     
     return render(request, 'base.html')

@login_required
def deslogar(request):
    auth.logout(request)
    return redirect('login')

@login_required
def criar_usuario(request):
     if request.user.is_staff or request.user.is_superuser:
          if request.method == 'POST':
               formulario = formCadastrarNovoUsuario(request.POST)
               if formulario.is_valid:
                    novo_usuario = formulario.save(commit=False)
                    senha_provisoria = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    novo_usuario.set_password(senha_provisoria)
                    novo_usuario.save()

                    # Enviar email para o usuario com a senha provisória
                    subject = 'Bem-vindo à Rudra Engenharia.'
                    message = f'Olá {novo_usuario.username},\n\nSeu cadastro foi realizado com sucesso!\n\nSua senha provisória é: {senha_provisoria}\n\nPor favor, faça login em nosso site e altere sua senha assim que possível.'
                    from_email = 'kyuenrique@gmail.com'  # Trocar para email da wizmart
                    to_email = novo_usuario.email
                    send_mail(subject, message, from_email, [to_email])

                    messages.success(request, 'Cadastro realizado com sucesso. Um email com a senha provisória foi enviado para o endereço fornecido.')
                    return redirect('pagina_inicial')

          else:
               formulario = formCadastrarNovoUsuario()
          return render(request, 'criar_usuario.html', {'formulario':formulario})
     else:
          messages.error(request, "Seu usuário não tem permissão para criar novos usuários. Entre em contato com um administrador.")
          return render(request, 'operacao_negada.html')

@login_required
def alterar_dados_usuario(request):
     if request.method == 'POST':
          formulario = formAlterarDadosUsuario(request.POST, instance=request.user)
          if formulario.is_valid():
               formulario.save()
               messages.success(request, "Seus dados foram alterados com sucesso.")
               return redirect('perfil_usuario')
     else:
          formulario = formAlterarDadosUsuario(instance=request.user)

     return render(request, 'alterar_dados_usuario.html', {'formulario':formulario})
     
@login_required
def perfil_usuario(request):
     dados_usuario = get_object_or_404(User, username=request.user)
     return render(request, 'perfil.html', {'dados_usuario':dados_usuario})