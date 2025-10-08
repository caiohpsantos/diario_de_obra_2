from django.db import models
from django.db.models.fields import CharField, IntegerField, BooleanField, DateTimeField, DateField

# Create your models here.
class Historico_Edicao(models.Model):
     '''
    Armazena as edições feitas nos contratos, obras, diarios e notificações

    Attributes:
        tipo(String): Especifica o que foi alterado (contrato, obra, diário ou notificação)
        tipo_id(Integer): Identificação do registro alterado com, no máximo, 15 caracteres
        descricao_alteracao(String): Frase que especifica como o registro era antes e como ficou depois
        usuario(String): Especifica o nome do usuário que fez a alteração
        timestamp(DateTime): Especifica quando o registro foi alterado, campo automático não é necessário inserir o valor.

    '''
     tipo = CharField(max_length=15, null=False) #string que especifica o que foi editado (contrato, obra, diario ou notificacao)
     tipo_id = IntegerField(null=False) #id que identifica o registro do tipo fornecido acima
     descricao_alteracao = CharField(max_length=400, null=False) # string que especifica o que foi editado, o que era antes e como ficou
     usuario = CharField(max_length=50, null=False) #especifica o usuario que fez a alteração
     timestamp = DateTimeField(auto_now=True) #Timestamp da alteração