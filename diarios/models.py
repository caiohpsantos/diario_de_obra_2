from django.db import models
from django.db.models.fields import CharField, IntegerField, DateTimeField
from django.db.models import ForeignKey
from obras.models import Obras


# Create your models here.


class Diarios(models.Model):
    '''
    Armazena os dados dos diarios de obra

    Attributes:
        id(Integer): Identificação única do diário, chave primária
        data(DateTime): Data que o diário registra. No formato dd/mm/aaaa
        clima_manha(String): Especifica o clima no turno da manhã com, no máximo, 20 caracteres
        clima_tarde(String): Especifica o clima no turno da tarde com, no máximo, 20 caracteres
        clima_noite(String): Especifica o clima no turno da noite com, no máximo, 20 caracteres
        clima_madrugada(String): Especifica o clima no turno da madrugada com, no máximo, 20 caracteres
        observacoes(String): Observações pontuais que não estão especificadas em outros campos com, no máximo,
        255 caracteres
        obra(ForeignKey): Identificação da obra a que este diário se refere, chave estrangeira
        
    '''
    opcoes = [("limpo", "Limpo"), ("nublado", "Nublado"), ("chuva","Chuva"), ("impraticavel","Impraticável")]
    data = DateTimeField()
    clima_manha = CharField(max_length=20, null=False, choices=opcoes)
    clima_tarde = CharField(max_length=20, null=False,  choices=opcoes)
    clima_noite = CharField(max_length=20, null=False,  choices=opcoes)
    clima_madrugada = CharField(max_length=20, null=False)
    observacoes = CharField(max_length=255, null=False)
    obra = models.ForeignKey(Obras, on_delete=models.DO_NOTHING, null=False)
    created_at = DateTimeField(auto_now_add=True)
    usuario_criador = CharField(max_length=100)

    def __str__(self):
        return f"{self.obra.contrato.nome} - {self.obra.nome} / DIÁRIO {self.id} de {self.data.strftime('%d/%m/%Y')}"

class ServicosPadrao(models.Model):
    '''
        Armazena os nomes dos serviços que serão usados nos diários

        Attributes:
            id(Integer): Identificação única do serviço padrão, chave primária
            descricao(String): Nome do serviço padrão com, no máximo 100 caracteres
    '''
    descricao = CharField(max_length=100, null=False)

    def __str__(self):
        return self.descricao

class Servicos(models.Model):
    '''
    Armazena os serviços registrados para o diário

    Attributes:
        id(Integer): Identificação única do serviço, chave primária
        servicos_padrao_id(Integer): Identificação do serviço escolhido das opções de serviço padrão, chave estrangeira
        item(Integer): Especifica a posição do item dentre os armazenados
        referencia(Integer): Especifica o local em que o serviço foi feito com, no máximo 100 caracteres
        diario_id(Integer): Especifica o diário no qual esse serviço está contido
    '''

    servicos_padrao = models.ForeignKey(ServicosPadrao, on_delete=models.DO_NOTHING)
    item = IntegerField()
    referencia = CharField(max_length=100, null=False)
    diario = ForeignKey(Diarios, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.servicos_padrao

class Efetivo_Direto_Padrao(models.Model):
    '''
        Armazena o efeito direto padrão a ser usado no diario

        Attributes:
            id(Integer): Identificação única do efetivo direto padrao, chave primária
            funcao(String): Especifica a função direta com, no máximo, 40 caracteres
            qtde(Integer): Especifica a quantidade de pessoas alocadas para essa função
            presente(Integer): Especifica quantos do total alocado estavam presentes no dia
    '''
    funcao = CharField(max_length=40, null=False)
    qtde = models.PositiveIntegerField(null=False)
    presente = models.PositiveIntegerField(null=False)

    @property
    def ausente(self):
        return self.qtde - self.presente
    
    @property
    def efetivo(self):
        return self.presente

    def __str__(self):
        return f"{self.funcao} | Qtde: {self.qtde} | Presente:{self.presente}"
    
class Efetivo_Direto(models.Model):        
    '''
        Armazena o efeito direto para o diario

        Attributes:
            id(Integer): Identificação única do efetivo direto, chave primária
            funcao(String): Especifica a função direta com, no máximo, 40 caracteres
            qtde(Integer): Especifica a quantidade de pessoas alocadas para essa função
            presente(Integer): Especifica quantos do total alocado estavam presentes no dia
            diario_id(Integer): Especifica o diario a que esse efetivo pertence, chave estrangeira
    '''
    funcao = CharField(max_length=40, null=False)
    qtde = IntegerField(null=False)
    presente = IntegerField(null=False)
    diario = ForeignKey(Diarios, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.funcao} | Qtde: {self.qtde} | Presente:{self.presente}"

class Efetivo_Indireto_Padrao(models.Model):
    '''
    Armazena o efetivo indireto padrão para ser usado no diario

    Attributes:
        id(Integer): Identificação única do efetivo indireto, chave primária
        funcao(String): Especifica a função indireta com, no máximo, 40 caracteres
        efetivo(Integer): Especifica a quantidade de pessoas alocadas para aquela função
    '''
     
    funcao = CharField(max_length=40, null=False)
    efetivo = IntegerField(null=False)

class Efetivo_Indireto(models.Model):
    '''
    Armazena o efetivo indireto registrado para o diario

    Attributes:
        id(Integer): Identificação única do efetivo indireto, chave primária
        funcao(String): Especifica a função indireta com, no máximo, 40 caracteres
        efetivo(Integer): Especifica a quantidade de pessoas alocadas para aquela função
        diario_id(Integer): Especifica o diário a que esse efetivo pertence
    '''
     
    funcao = CharField(max_length=40, null=False)
    efetivo = IntegerField(null=False)
    diario = ForeignKey(Diarios, on_delete=models.DO_NOTHING)

    



