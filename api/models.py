from django.db import models
from datetime import datetime, timedelta

class Pedido(models.Model):
    # criado_em = models.DateTimeField(auto_now_add=True)
    class StatusChoices(models.TextChoices):
        ENTREGUE_AUTOMATICAMENTE = "ENTREGUE_AUTOMATICAMENTE", "Entregue_automaticamente"
        ENTREGUE = "ENTREGUE", "Entregue"
        FINALIZADO = "FINALIZADO", "Finalizado"
        PENDENTE = "PENDENTE", "Pendente"
    
    data = models.DateTimeField()
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=24, choices=StatusChoices.choices, default=StatusChoices.PENDENTE)

    def __str__(self) -> str:
        # return self.criado_em.strftime("%d/%m/%Y, %H:%M:%S")
        return self.data.strftime("%d/%m/%Y, %H:%M:%S")

class Comida(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    identificador_nome = models.CharField(max_length=150, unique=True)
    categoria = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

class PedidoComida(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="pedido_comida", on_delete=models.CASCADE)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        unique_together = [['pedido', 'comida']]

    def __str__(self) -> str:
        return self.comida.nome