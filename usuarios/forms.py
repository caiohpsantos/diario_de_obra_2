from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

#Personaliza o formulário de criação de usuário padrão com labels melhor trabalhados e textos explicativos
class formCadastrarNovoUsuario(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório pois será enviado um email para o cliente terminar o cadastro")
    first_name = forms.CharField(max_length=50, label='Nome', required=True)
    last_name = forms.CharField(max_length=50, label="Sobrenome", required=False)
    is_staff = forms.BooleanField(label='É administrador', help_text='Administradores podem criar ou desativar usuários e prestadores de serviços', required=False)
    password1 = forms.CharField(widget=forms.HiddenInput(), required=False)
    password2 = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']

#Personaliza o formulário de criação de usuário padrão com labels melhor trabalhados e textos explicativos
class formAlterarDadosUsuario(forms.ModelForm):
    is_active = forms.BooleanField(required=False, label='Ativo', help_text="Desmarque para que o usuário fique desativado no sistema")
    username = forms.CharField(max_length=50, label="Usuário", help_text="Será usado para o login")
    first_name = forms.CharField(max_length=50, label="Nome")
    last_name = forms.CharField(max_length=50, label="Sobrenome")
    email = forms.EmailField(help_text="Obrigatório para recuperação de senha")


    class Meta:
        model = User
        fields = ['is_active', 'username', 'first_name', 'last_name', 'email']

#Altera o formulário padrão de envio de email para troca de senha inserindo o email do usuário no input automaticamente
class formTrocaSenhacomEmailAutomatico(PasswordResetForm):
    def __init__(self, user=None, *args, **kwargs):
            # Chama o inicializador do formulário pai
            super().__init__(*args, **kwargs)
            # Define o e-mail inicial como o e-mail do usuário logado, se estiver autenticado
            if user is not None and user.is_authenticated:
                self.fields['email'].initial = user.email