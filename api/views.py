from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

from datetime import datetime, timedelta
from django.utils import timezone

class PedidoComidaView(APIView):
    #  {
    #       "comidas": 
    #           [
    #               {
    #                   "nome": "<comida_nome>", 
    #                   "quantidade": "<comida_quantidade>"
    #               },
    #               {
    #                   "nome": "<comida_nome2>", 
    #                   "quantidade": "<comida_quantidade2>"
    #               }
    #           ] 
    #   }
    def post(self, request, format=None):
        time = timezone.now() - timedelta(hours=3)
        pedido = Pedido.objects.create(data=time)
        # pedido = Pedido.objects.get(id=1)

        for comida in request.data["comidas"]:
            comida_instance = get_object_or_404(Comida, nome=comida["nome"])
            pedidoComida_serializer = PedidoComidaSerializer(data={"pedido_id":pedido.id, 
                                                                   "comida_id":comida_instance.id,
                                                                   "quantidade":comida["quantidade"]})
   
            pedidoComida_serializer.is_valid(raise_exception=True)
            pedidocomida = pedidoComida_serializer.save()
            print(pedidocomida)

        return Response()

class PedidoView(APIView):
    def get(self, request, format=None):
        return Response({"ok":"ok"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        time = timezone.now() - timedelta(hours=12)
        print(time.strftime("%d/%m/%Y, %H:%M:%S"))
        Pedido.objects.create(data=time)
        return Response({"ok":"ok"}, status=status.HTTP_200_OK)


class ComidaView(APIView):
    def get(self, request, format=None):
        return Response({"ok":"ok"}, status=status.HTTP_200_OK)
    
    # nome, quantidade (estoque)
    def post(self, request, format=None):
        comida_serializer = ComidaSerializer(data=request.data)
        comida_serializer.is_valid(raise_exception=True)
        comida_serializer.save()

        return Response({"detail":"success", "comida": comida_serializer.data}, status=status.HTTP_201_CREATED)