from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models.fields import CharField, DateField
from django.db.models import ForeignKey
from contratos.models import Contratos


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

    ANDAMENTO = "andamento"
    CONCLUIDA = "concluida"
    PARADA = "parada"

    SITUACAO_CHOICES = [
        (ANDAMENTO, "Em andamento"),
        (CONCLUIDA, "Concluída"),
        (PARADA, "Parada"),
    ]

    nome = CharField(max_length=100, null=False)
    local = CharField(max_length=200, null=False)
    inicio = DateField(null=False)
    termino = DateField(null=False)
    situacao = CharField(max_length=20,
        choices=SITUACAO_CHOICES,
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
        prazo_delta = relativedelta(self.termino, date.today())
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
