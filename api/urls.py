from django.urls import path, include
from . import views

urlpatterns = [
    path("api/pedidocomida/", views.PedidoComidaView.as_view(), name="pedido_comida"),
    path("api/comida/", views.ComidaView.as_view(), name="comida"),
    path("api/pedido/", views.PedidoView.as_view(), name="pedido")
]
