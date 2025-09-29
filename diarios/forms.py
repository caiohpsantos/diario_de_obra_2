from django import forms
from .models import Contratos, Obras

#formulários relativos aos contratos
class formCadastraContrato(forms.Form):
    '''
    Classe responsável pela criação do formulário de cadastro de contrato.
    Nesta classe o campo "ativo" não aparece pois ele é True no momento do cadastro.

    Campos: numero, nome, cliente, dia_inicia_relatorio, dia_finaliza_relatorio
    '''
    numero = forms.CharField(max_length=15,
                             strip=True,
                             required=True,
                             label="Número do contrato",
                             help_text="Aceita letra e símbolos especiais. Não pode ser vazio.",
                             widget=forms.TextInput(attrs={
                                'class': 'form-control form-control-sm',
        }))
    
    nome = forms.CharField(max_length=200,
                             strip=True,
                             required=True,
                             label="Nome",
                             help_text="Nome interno do contrato. Limite de 200 caracteres")
    
    cliente = forms.CharField(max_length=200,
                             strip=True,
                             required=True,
                             label="Cliente",
                             help_text="Especificação do cliente. Limite de 200 caracteres")
    
    dia_inicia_relatorio = forms.IntegerField(max_value=31,
                                              min_value=1,
                                              required=True,
                                              label="Dia do mês que inicia o relatório",
                                              help_text="Digite apenas o dia. Aceita somente números.")
    
    
    dia_finaliza_relatorio = forms.IntegerField(max_value=31,
                                              min_value=1,
                                              required=True,
                                              label="Dia do mês que finaliza o relatório",
                                              help_text="Digite apenas o dia. Aceita somente números.")
    

    class Meta:
        model = Contratos
        fields = [
            'numero', 'nome', 'cliente', 'dia_inicia_relatorio',
            'dia_finaliza_relatorio'
        ]
    
    def clean_numero(self):
        numero = self.cleaned_data["numero"]
        if Contratos.objects.filter(numero=numero).exists():
            raise forms.ValidationError("Este número de contrato já está em uso.")
        return numero

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if Contratos.objects.filter(nome=nome).exists():
            raise forms.ValidationError("Este nome de contrato já está em uso.")
        return nome
     
class formEditaContrato(forms.Form):
    '''
    Classe responsável pela criação do formulário de edição de contrato.

    Campos: ativo, numero, nome, cliente, dia_inicia_relatorio, dia_finaliza_relatorio
    '''
    
    ativo = forms.BooleanField(
        label="Status",
        required=False
    )
    numero = forms.CharField(max_length=15,
                             strip=True,
                             required=True,
                             label="Número do contrato",
                             help_text="Aceita letra e símbolos especiais. Não pode ser vazio.",
                             )
    
    nome = forms.CharField(max_length=200,
                             strip=True,
                             required=True,
                             label="Nome",
                             help_text="Nome interno do contrato. Limite de 200 caracteres")
    
    cliente = forms.CharField(max_length=200,
                             strip=True,
                             required=True,
                             label="Cliente",
                             help_text="Especificação do cliente. Limite de 200 caracteres")
    
    dia_inicia_relatorio = forms.IntegerField(max_value=31,
                                              min_value=1,
                                              required=True,
                                              label="Dia do mês que inicia o relatório",
                                              help_text="Digite apenas o dia. Aceita somente números.")
    
    
    dia_finaliza_relatorio = forms.IntegerField(max_value=31,
                                              min_value=1,
                                              required=True,
                                              label="Dia do mês que finaliza o relatório",
                                              help_text="Digite apenas o dia. Aceita somente números.")
    
   
    class Meta:
        model = Contratos
        fields = [
            'ativo','numero', 'nome', 'cliente', 'dia_inicia_relatorio',
            'dia_finaliza_relatorio'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        inicia = cleaned_data.get("dia_inicia_relatorio")
        finaliza = cleaned_data.get("dia_finaliza_relatorio")

        if inicia is not None and finaliza is not None:
            if inicia <= finaliza:
                raise forms.ValidationError(
                    "Dia inicial do relatório deve ser maior que o dia final. "
                    "Exemplo: Se inicia no dia 2, deve terminar no dia 1."
                )
        return cleaned_data

#formulários relativos às obras
class formCadastraObra(forms.ModelForm):
    '''
    Classe responsável pela criação do formulário de cadastro de novas obras.
    Campos: situacao, contrato, nome, local, inicio, termino, empresa_responsavel 
    '''
    class Meta:
        model = Obras
        fields = ['situacao', "contrato", "nome", "local", "inicio", "termino", "empresa_responsavel"]
        widgets = {
            "inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "termino": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "empresa_responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "situacao": forms.Select(attrs={"class": "form-select"}), #dropdown de situações
            "contrato": forms.Select(attrs={"class": "form-select"}),  # dropdown de contratos
        }

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if Obras.objects.filter(nome=nome).exists():
            raise forms.ValidationError("Este nome de obra já está em uso.")
        return nome