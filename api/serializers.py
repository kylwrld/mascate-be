from rest_framework import serializers
from .models import *

class ComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comida
        fields = ["nome", "identificador_nome", "categoria", "preco"]
        optional_fields = ['preco', ]

class PedidoComidaSerializer(serializers.ModelSerializer):
    pedido_id = serializers.IntegerField()
    comida_id = serializers.IntegerField()
    nome = serializers.SerializerMethodField()

    class Meta:
        model = PedidoComida
        fields = ["pedido_id", "comida_id", "nome", "quantidade"]

    def get_nome(self, instance: PedidoComida):
        nome = instance.comida.nome
        return nome

    # def to_representation(self, instance):
    #     print(instance, self.Meta.model)
    #     super(PedidoComidaSerializer, self).to_representation(instance)

    def create(self, validated_data):
        
        return super().create(validated_data)
    
class PedidoSerializer(serializers.ModelSerializer):
    pedidoscomida = PedidoComidaSerializer(source="pedido_comida", many=True)

    class Meta:
        model = Pedido
        fields = ["id", "data", "total", "pedidoscomida"]

class RelatorioSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    
    class Meta:
        model = PedidoComida
        fields = ["nome", "quantidade"]

    def get_nome(self, instance: PedidoComida):
        nome = instance.comida.nome
        return nome