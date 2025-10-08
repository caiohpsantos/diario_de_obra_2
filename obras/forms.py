from django import forms
from .models import Obras
from contratos.models import Contratos


class formCadastraObra(forms.ModelForm):
    '''
    Classe responsável pela criação do formulário de cadastro de novas obras.
    Campos: situacao, contrato, nome, local, inicio, termino, empresa_responsavel 
    '''
    class Meta:
        model = Obras
        fields = ['situacao', "contrato", "nome", "local", "inicio", "termino", "empresa_responsavel"]
        widgets = {
            "inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "empresa_responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "situacao": forms.Select(attrs={"class": "form-select"}), #dropdown de situações
            "contrato": forms.Select(attrs={"class": "form-select"}),  # dropdown de contratos
        }
        input_formats = {
        "inicio": ["%Y-%m-%d"],
        "termino": ["%Y-%m-%d"],
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contrato'].queryset = Contratos.objects.filter(ativo=True)

    def clean_nome(self):
        nome = self.cleaned_data["nome"]
        if Obras.objects.filter(nome=nome).exists():
            raise forms.ValidationError("Este nome de obra já está em uso.")
        return nome
    
class formEditaObra(forms.ModelForm):
    '''
    Classe responsável pela criação do formulário de edição de obras.
    Campos: situacao, contrato, nome, local, inicio, termino, empresa_responsavel 
    '''
    class Meta:
        model = Obras
        fields = ['situacao', "contrato", "nome", "local", "inicio", "termino", "empresa_responsavel"]
        widgets = {
            "inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "termino": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "empresa_responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "situacao": forms.Select(attrs={"class": "form-select"}), #dropdown de situações
            "contrato": forms.Select(attrs={"class": "form-select"}),  # dropdown de contratos
        }
        input_formats = {
        "inicio": ["%Y-%m-%d"],
        "termino": ["%Y-%m-%d"],
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtra contratos ativos
        contratos_qs = Contratos.objects.filter(ativo=True)

        # Se estiver editando uma obra existente, inclui o contrato atual mesmo se estiver inativo
        if self.instance and self.instance.pk and self.instance.contrato:
            contrato_atual = self.instance.contrato
            if contrato_atual.ativo != True:
                contratos_qs = Contratos.objects.filter(
                    pk=contrato_atual.pk
                ) | contratos_qs  # Une o contrato atual ao queryset filtrado

        self.fields['contrato'].queryset = contratos_qs

    
    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        instance = getattr(self, 'instance', None)

        # Se for um novo registro (sem instance.id)
        if not instance or not instance.pk:
            if Obras.objects.filter(nome=nome).exists():
                raise forms.ValidationError("Este nome de obra já está em uso.")
        else:
            # Se for edição, só valida se o nome mudou
            if nome != instance.nome:
                if Obras.objects.filter(nome=nome).exists():
                    raise forms.ValidationError("Este nome de obra já está em uso.")

        return nome
    