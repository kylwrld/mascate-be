from django.db import models
from datetime import datetime, timedelta

class Pedido(models.Model):
    # criado_em = models.DateTimeField(auto_now_add=True)
    data = models.DateTimeField()

    def __str__(self) -> str:
        # return self.criado_em.strftime("%d/%m/%Y, %H:%M:%S")
        return self.data.strftime("%d/%m/%Y, %H:%M:%S")

class Comida(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    quantidade = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

class PedidoComida(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        unique_together = [['pedido', 'comida']]