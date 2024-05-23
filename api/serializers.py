from rest_framework import serializers
from .models import *

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ["data"]

class ComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comida
        fields = ["nome", "quantidade"]

        extra_kwargs = {"quantidade": {"required": False}}

class PedidoComidaSerializer(serializers.ModelSerializer):
    pedido_id = serializers.IntegerField()
    comida_id = serializers.IntegerField()
    
    class Meta:
        model = PedidoComida
        fields = ["pedido_id", "comida_id", "quantidade"]

    def create(self, validated_data):
        
        return super().create(validated_data)