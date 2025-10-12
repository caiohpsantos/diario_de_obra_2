import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

def caminho_foto(instance, filename):
    """
    Define dinamicamente o caminho e nome do arquivo da foto.
    Exemplo:
    fotos/ContratoA/ObraX/2025-10-03/foto_ContratoA_ObraX_2025-10-03_001.jpg
    """

    # Extrai informações do relacionamento
    contrato_nome = (
        instance.obra.contrato.nome if hasattr(instance.obra, "contrato") and instance.obra.contrato else "sem_contrato"
    )
    obra_nome = instance.obra.nome if instance.obra else "sem_obra"

    # Formata nomes para evitar caracteres inválidos em caminhos
    contrato_nome = contrato_nome.replace(" ", "_").replace("/", "_")
    obra_nome = obra_nome.replace(" ", "_").replace("/", "_")

    # Data da captura (ou data atual se não houver)
    data = instance.data_captura.strftime("%Y-%m-%d") if instance.data_captura else timezone.now().strftime("%Y-%m-%d")

    # Contador (para evitar nomes duplicados)
    numero = instance.id or "novo"

    # Extensão original do arquivo
    ext = os.path.splitext(filename)[1]

    # Monta o nome e o caminho
    nome_arquivo = f"foto_{contrato_nome}_{obra_nome}_{data}_{numero}{ext}"
    caminho = os.path.join("fotos", contrato_nome, obra_nome, data, nome_arquivo)

    return caminho

class Fotos(models.Model):
    arquivo = models.ImageField(upload_to=caminho_foto)
    descricao = models.CharField(max_length=255, blank=True)
    data_captura = models.DateTimeField(default=timezone.now)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    obra = models.ForeignKey('obras.Obras', on_delete=models.CASCADE, related_name='fotos')

    # Relação genérica — permite vincular esta foto a qualquer modelo (Diário, Notificação, etc)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_captura', 'criada_em']

    def __str__(self):
        return f"Foto {self.id} - {self.obra.nome if self.obra else 'Sem obra'}"