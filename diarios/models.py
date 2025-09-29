from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.fields import CharField, IntegerField, BooleanField, DateTimeField, DateField
from django.db.models import ForeignKey

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

class Contratos(models.Model):
    '''
        Armazena os dados do contrato

        Attributes:
            numero(Sring): Número do contrato, é string pois pode conter símbolos diversos. Pode ter,
            no máximo, 15 caracteres. Campo único
            nome(String): Nome completo do contrato  com, no máximo, 200 caracteres. Campo único
            cliente(String): Nome completo do cliente do contrato  com, no máximo, 200 caracteres
            dia_inicia_relatorio(Integer): Dia em que inicia a contabilização dos diários (abre o período/mês)
            dia_finaliza_relatorio(Integer): Dia em que finaliza a contabilização dos diários (fecha o período/mês)
            ativo(Boolean): especifica se o contrato está ativo(verdadeiro) ou inativo(falso)
        '''
    numero = CharField(max_length=15, null=False, unique=True)
    nome = CharField(max_length=200, null=False)
    cliente = CharField(max_length=200, null=False)
    dia_inicia_relatorio = IntegerField(null=False)
    dia_finaliza_relatorio = IntegerField(null=False)
    ativo = BooleanField(default=True)

    def __str__(self):
        return f"{self.numero}: {self.nome}"  # Define o formato de exibição do contrato

class Obras(models.Model):
    '''
    Armazena os dados das obras

    Attributes:
        id(Integer): Identificação única da obra, chave primária
        nome(String): Nome completo do Obra com, no máximo, 100 caracteres
        local(String): Especificação do local em que ela acontece com, no máximo, 200 caracteres
        inicio(DateTime): Especifica a data em que esta obra começou (não é a data do contrato)
        termino(DateTime): Especifica a previsão de término da obra
        situacao(String): Especifica se a obra está: Em andamento, Concluída ou Parada
        contrato(ForeignKey): Instãncia do contrato a que esta obra pertence. Chave estrangeira da tabela 'contrato'.
        empresa_responsavel(String): Empresa responsável pela execução do contrato (construtora/empreiteira)
            com, no máximo, 200 caracteres
    '''

    nome = CharField(max_length=100, null=False)
    local = CharField(max_length=200, null=False)
    inicio = DateField(null=False)
    termino = DateField(null=False)
    situacao = CharField(max_length=20,
        choices=[("andamento", "Em andamento"),
                 ("concluida", "Concluída"),
                 ("parada", "Parada")],
        default="andamento")
    contrato = ForeignKey(Contratos, on_delete=models.DO_NOTHING, null=False)
    empresa_responsavel = CharField(max_length=200, null=False)

    def __str__(self):
        return f"Obra {self.nome} do contrato {self.contrato.nome if self.contrato else 'Sem contrato associado'}"

    @property
    def prazo_entrega_dias(self):
        '''
        Calcula qtos dias faltam para o término da obra.
        Attributes:
            return: total_dias(int)
        '''
        return (self.termino - date.today()).days
    
    @property
    def prazo_entrega(self):
        '''
        Calcula o prazo de entrega da obra.
        Attributes:
            return: tempo_restante(string): String contando qto tempo falta para entrega em anos, meses e dias.
        '''
        prazo_delta = relativedelta(self.termino - date.today())
        partes = []
        if prazo_delta.years == 1:
            partes.append(f"{prazo_delta.years} ano")
        if prazo_delta.years > 1:
            partes.append(f"{prazo_delta.years} anos")    
        if prazo_delta.months == 1:
            partes.append(f"{prazo_delta.months} mês")
        if prazo_delta.months > 1:
            partes.append(f"{prazo_delta.months} meses")
        if prazo_delta.days == 1:
            partes.append(f"{prazo_delta.days} dia")
        if prazo_delta.days > 1:
            partes.append(f"{prazo_delta.days} dias")
        tempo_restante = ", ".join(partes) if partes else "0 dias"
        return tempo_restante
    
    @property
    def tempo_obra_dias(self):
        '''
        Calcula qtos dias se passaram desde o início da obra.
        Attributes:
        
            return: total_dias(int)
        '''
        #cálculo de dias corridos sem considerar anos, meses...
        total_dias = (date.today()-self.inicio).days
        return total_dias

    @property
    def tempo_obra(self):
        '''
        Calcula o tempo que se passou desde o início da obra.
        
        Attributes:

            return: tempo_decorrido(String):Retorna uma string com os anos, meses e dias.
        '''
        decorrido_delta = relativedelta(date.today(), self.inicio)
        partes = []
        if decorrido_delta.years == 1:
            partes.append(f"{decorrido_delta.years} ano")
        if decorrido_delta.years > 1:
            partes.append(f"{decorrido_delta.years} anos")    
        if decorrido_delta.months == 1:
            partes.append(f"{decorrido_delta.months} mês")
        if decorrido_delta.months > 1:
            partes.append(f"{decorrido_delta.months} meses")
        if decorrido_delta.days == 1:
            partes.append(f"{decorrido_delta.days} dia")
        if decorrido_delta.days > 1:
            partes.append(f"{decorrido_delta.days} dias")
        tempo_decorrido = ", ".join(partes) if partes else "0 dias"
        return tempo_decorrido

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

    data = DateTimeField()
    clima_manha = CharField(max_length=20, null=False)
    clima_tarde = CharField(max_length=20, null=False)
    clima_noite = CharField(max_length=20, null=False)
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
    diario = models.ForeignKey(Diarios, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.servicos_padrao

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
    diario = models.ForeignKey(Diarios, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.funcao} | Qtde: {self.qtde} | Presente:{self.presente}"
    
# class Efetivo_Indireto(models.Model):
    



