from django.urls import path, include
from . import views

urlpatterns = [
    path("api/pedidocomida/", views.PedidoComidaView.as_view(), name="pedido_comida"),
    path("api/pedidocomida/<int:hour>/", views.PedidoComidaView.as_view(), name="pedido_comida"),
    path("api/comida/", views.ComidaView.as_view(), name="comida"),
    path("api/pedido/", views.PedidoView.as_view(), name="pedido"),
    path("api/pedido/<int:pk>/", views.PedidoView.as_view(), name="pedido_pk"),
    path("api/relatorio/dia/<str:dia>/", views.RelatorioView.as_view(), name="relatorio_dia"),
    path("api/relatorio/semanal/", views.RelatorioView.as_view(), name="relatorio_semanal")
]
