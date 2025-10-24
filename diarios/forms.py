from datetime import date
from django import forms
from django.forms import modelformset_factory
from .models import Diarios, ServicosPadrao, Servicos, Efetivo_Direto, Efetivo_Direto_Padrao
from .models import Efetivo_Indireto, Efetivo_Indireto_Padrao
from fotos.models import Fotos
from contratos.models import Contratos

class DiarioForm(forms.ModelForm):
    '''
    Classe responsável pela criação do formulário de cadastro de um novo diário.
    Campos: contrato, obra, data, clima(manha,tarde,noite,madrugada) e observações
    '''
    #Gera o campo para escolher o contrato com os que estiverem ativos
    contratos = forms.ModelChoiceField(
        queryset=Contratos.objects.filter(ativo=True),
        label="Contrato",
        empty_label='-- Selecione o contrato --',
        required=True,
        widget=forms.Select(attrs={"class": "form-select form-select-sm", "id": "contratoSelect"})
    )
    #Gera o campo para seleção da obra sem opções. Código javascript atualizará o campo
    #buscando as obras em execução na url contratos/obras_por_contrato/
    obra = forms.ModelChoiceField(
        queryset=None,
        label="Obra",
        empty_label='-- Selecione a obra --',
        required=True,
        widget=forms.Select(attrs={"class": "form-select form-select-sm", "id": "obraSelect"})
    )

    #Gera as opções de clima
    CLIMA_CHOICES = [
        ("limpo", "Limpo"),
        ("nublado", "Nublado"),
        ("chuva", "Chuva"),
        ("impraticavel", "Impraticável"),
    ]

    clima_manha = forms.ChoiceField(
        choices=CLIMA_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Clima da Manhã"
    )
    clima_tarde = forms.ChoiceField(
        choices=CLIMA_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Clima da Tarde"
    )
    clima_noite = forms.ChoiceField(
        choices=CLIMA_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Clima da Noite"
    )
    clima_madrugada = forms.ChoiceField(
        choices=CLIMA_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Clima da Madrugada"
    )

    class Meta:
        model = Diarios
        fields = [
            "contratos",
            "obra",
            "dia",
            "clima_manha",
            "clima_tarde",
            "clima_noite",
            "clima_madrugada",
            "observacoes"
        ]
        widgets = {
            #mudança de data para dia para tratar erros de compatibilidade com palavras reservadas
            #format é atribuído dessa forma para compatibilidade com html 5
            #o campo value do input recebe a dia atual
            "dia":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control",
                                                            "value":date.today().strftime("%Y-%m-%d")}),
        }
        input_formats = {
        "dia": ["%Y-%m-%d"]}

class ServicosForm(forms.ModelForm):
    '''
    Classe responsável por gerar o formulário de registro dos serviços prestados
    Campos: servico_padrao_id, item e referencia(descrição mais detalhada da execução ou local)
    '''
    
    class Meta:
        model = Servicos
        fields = ["servicos_padrao", 'item', "referencia"]
        widgets = {
            "servicos_padrao": forms.Select(attrs={"class": "form-select form-select-sm"}),
            #item é a ordem em que o serviço deve aparecer, campo automático e não editável
            "item": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 1, "disabled":"disabled"}),
            "referencia": forms.TextInput(attrs={"class": "form-control form-control-sm", "maxlength": 100}),
        }
        labels = {
            "servicos_padrao": "Serviço Padrão",
            "referencia": "Referência",
        }

#form set do Serviços para criar vários campos pois podem haver vários serviços executados
ServicoFormSet = modelformset_factory(
    Servicos,
    form=ServicosForm,
    extra=1,           # começa com 1 formulário visível
    max_num=14,
    can_delete=True    # permite exclusão
)

class EfetivoDiretoForm(forms.ModelForm):
    '''
    Cria o formulário de registro do Efetivo direto para os diários
    Campos: funcao, qtde e presente
    Os dados Ausente e Efetivo Total são calculados com funções decoradas na model
    '''
    class Meta:
        model = Efetivo_Direto
        fields = ["funcao", "qtde", "presente"]
        widgets = {
            "funcao": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "qtde": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 0}),
            "presente": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 0})
        }

# Formset (permite múltiplos registros de efetivo direto por diário)
EfetivoDiretoFormSet = modelformset_factory(
    Efetivo_Direto,
    form=EfetivoDiretoForm,
    extra=int(Efetivo_Direto_Padrao.objects.all().count())
)

class EfetivoIndiretoForm(forms.ModelForm):
    '''
    Classe responsável por gerar formulário de cadastro do efetivo indireto
    campos: função e efetivo
    '''
    class Meta:
        model = Efetivo_Indireto
        fields = ['funcao', 'efetivo']
        widgets = {
            "funcao": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "efetivo": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 0})
        }

EfetivoIndiretoFormSet = modelformset_factory(
    Efetivo_Indireto,
    EfetivoIndiretoForm,
    extra=int(Efetivo_Indireto_Padrao.objects.all().count())
)