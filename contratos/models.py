from django.db import models
from django.db.models.fields import CharField, IntegerField, BooleanField

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