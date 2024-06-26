from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

from datetime import datetime, timedelta
from django.utils import timezone
from django.db import reset_queries
from django.db import connection

from itertools import chain


class PedidoComidaView(APIView):
    def get(self, request, format=None):
        time = timezone.now() - timedelta(hours=3) # brazil time

        h_10_00 = datetime(time.year, time.month, time.day, 10, 0, tzinfo=time.tzinfo)
        h_11_59 = datetime(time.year, time.month, time.day, 11, 59, tzinfo=time.tzinfo)
        h_23_59 = datetime(time.year, time.month, time.day, 23, 59, tzinfo=time.tzinfo)
        previous_day_23_59 = datetime(time.year, time.month, time.day-1, 23, 59, tzinfo=time.tzinfo)

        if time > h_11_59 and time < h_23_59:
            pedidos = Pedido.objects.filter(data__range=(previous_day_23_59, h_11_59))

        elif time < h_11_59:
            previous_11_59 = datetime(time.year, time.month, time.day-1, 11, 59, tzinfo=time.tzinfo)
            pedidos = Pedido.objects.filter(data__range=(previous_11_59, previous_day_23_59))


        pedidos_serializer = PedidoSerializer(pedidos, many=True) 
        return Response({"detail":"success", "pedidos":pedidos_serializer.data}, status=status.HTTP_200_OK)
        
    #  {
    #       "comidas":
    #           [
    #               {
    #                   "identificador_nome": "<comida_nome>",
    #                   "quantidade": "<comida_quantidade>"
    #               },
    #               {
    #                   "nome": "<comida_nome2>",
    #                   "quantidade": "<comida_quantidade2>"
    #               }
    #           ]
    #   }
    def post(self, request, hour=None, format=None):
        time = timezone.now() - timedelta(hours=3)
        if hour is not None:
            time -= timedelta(hours=hour)

        pedido = Pedido.objects.create(data=time)

        # total = 0
        for comida in request.data["comidas"]:
            comida_instance = get_object_or_404(Comida, identificador_nome=comida["identificador_nome"])
            pedidoComida_serializer = PedidoComidaSerializer(data={"pedido_id":pedido.id, 
                                                                   "comida_id":comida_instance.id,
                                                                   "quantidade":comida["quantidade"]})
   
            pedidoComida_serializer.is_valid(raise_exception=True)
            pedidocomida = pedidoComida_serializer.save()
            # total += comida_instance.preco

        # pedido.total = total
        pedido.save()

        pedido_serializer = PedidoSerializer(pedido)
        return Response({"detail":"success", "pedido":pedido_serializer.data}, status=status.HTTP_201_CREATED)

class PedidoView(APIView):
    def get(self, request, pk=None, format=None):
        if pk is not None:
            pedido = get_object_or_404(Pedido, pk=pk)
            pedido_serializer = PedidoSerializer(pedido)
            return Response({"detail":"success", "pedido":pedido_serializer.data}, status=status.HTTP_200_OK)
        
        pedidos = Pedido.objects.all()

        pedidos_serializer = PedidoSerializer(pedidos, many=True) 
        return Response({"detail":"success", "pedidos":pedidos_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        time = timezone.now() - timedelta(hours=3)

        Pedido.objects.create(data=time)
        return Response({"ok":"ok"}, status=status.HTTP_200_OK)
    
    def patch(self, request, pk, format=None):
        pedido = get_object_or_404(Pedido, pk=pk)
        pedido_serializer = PedidoSerializer(pedido, data=request.data, partial=True)
        pedido_serializer.is_valid(raise_exception=True)
        pedido = pedido_serializer.save()
        return Response({"detail":"success", "pedido":pedido_serializer.data}, status=status.HTTP_201_CREATED)

class ComidaView(APIView):
    def get(self, request, format=None):
        comidas = Comida.objects.order_by("nome")
        comidas_serializer = ComidaSerializer(comidas, many=True)

        return Response({"detail":"success", "data":comidas_serializer.data}, status=status.HTTP_200_OK)
    
    # nome, quantidade (estoque)
    def post(self, request, format=None):
        comida_serializer = ComidaSerializer(data=request.data)
        comida_serializer.is_valid(raise_exception=True)
        comida_serializer.save()

        return Response({"detail":"success", "comida": comida_serializer.data}, status=status.HTTP_201_CREATED)

from django.db.models import Sum

class RelatorioView(APIView):
    def get(self, request, dia=None, format=None):
        if dia is not None:
            return Response({"pedidos":self.dia(request, format, dia)})

        return Response({"pedidos":self.semanal(request, format)})


    def dia(self, request, format, dia):
        dias = {"segunda":0, "terca":1, "quarta":2, "quinta":3, "sexta":4, "sabado":5, "domingo":6}
        dia = dias[dia]
        time = timezone.now() - timedelta(hours=3)

        if dia > time.weekday():
            day_to_fetch_start = datetime(time.year, time.month, time.day+((dia - time.weekday())), 0, 0, 0, tzinfo=time.tzinfo)
        elif dia == 0:
            day_to_fetch_start = datetime(time.year, time.month, time.day-time.weekday(), 0, 0, 0, tzinfo=time.tzinfo)
        else:
            day_to_fetch_start = datetime(time.year, time.month, time.day-((time.weekday() - dia)), 0, 0, 0, tzinfo=time.tzinfo)
        day_to_fetch_end = datetime(day_to_fetch_start.year, day_to_fetch_start.month, day_to_fetch_start.day, 23, 59, 59, tzinfo=day_to_fetch_start.tzinfo)

        comidas = PedidoComida.objects.filter(pedido__data__range=(day_to_fetch_start, day_to_fetch_end)).values("comida__nome").order_by("comida__nome").annotate(quantidade=Sum("quantidade"))

        d = []
        for f in comidas:
            d.append({"nome":f["comida__nome"], "quantidade":f["quantidade"]})
        return d

    def semanal(self, request, format=None):
        time = timezone.now() - timedelta(hours=3)
        time -= timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

        start = time - timedelta(days=time.weekday())
        end = start + timedelta(days=6)
        end = datetime(end.year, end.month, end.day, 23, 59, 59, tzinfo=end.tzinfo)

        dias = [(start, datetime(start.year, start.month, start.day, 23, 59, 59, tzinfo=time.tzinfo))]
        for i in range(1, 6):
            dias.append((datetime(start.year, start.month, start.day+i, 0, 0, 0, tzinfo=time.tzinfo), datetime(start.year, start.month, start.day+i, 23, 59, 59, tzinfo=time.tzinfo)))
        dias.append((datetime(start.year, start.month, start.day+6, 0, 0, 0, tzinfo=time.tzinfo), end))

        dias_comidas = []
        for dia in dias:
            dias_comidas.append(PedidoComida.objects.filter(pedido__data__range=dia))

        result = []
        for intervalo in dias_comidas:
            result.append(intervalo.values("comida__nome").order_by("comida__nome").annotate(quantidade=Sum("quantidade")))

        dicti = {}
        for lista in result:
            for obj in lista:
                if dicti.get(obj["comida__nome"], False) == False:
                    dicti[obj["comida__nome"]] = []
                    dicti[obj["comida__nome"]].append(obj["quantidade"])
                else:
                    dicti[obj["comida__nome"]].append(obj["quantidade"])

        # for lista in result:
        #     for obj in lista:
        #         for key in dicti.keys():
        #             if obj.get(key, False) == False:
        #                 dicti[key].append(0)
        #                 pass
                
                

        return dicti