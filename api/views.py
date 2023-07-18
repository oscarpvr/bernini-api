#  from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework import serializers

from .serializer import ProductSerializer, OrderSerializer, OrderLinesSerializer
from .models import Product, Order, OrderLines

# Implemento la autenticación por token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

# Implemento la caché
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet


# Create your views here.

# Listar productos
class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization",))
    def dispatch(self, *args, **kwargs):
       return super(ProductsViewSet, self).dispatch(*args, **kwargs)


class PedidoLineaSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    sell_cost = serializers.DecimalField(max_digits=7, decimal_places=2)

class PedidoSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    address = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()

class CreateOrdersSerializer(serializers.Serializer):
    pedido = PedidoSerializer()
    pedido_lineas = PedidoLineaSerializer(many=True)


# Realizar un pedido
class CreateOrdersViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateOrdersSerializer,
        responses={200: 'Success'}
    )
    @transaction.atomic
    def create(self, request):
        # Recupero la información de los datos anidados a "pedido" y "pedido_lineas" del json y los separo para
        # sus correspondientes tablas
        order_data = request.data.get('pedido')
        order_lines_data = request.data.get('pedido_lineas')

        # Compruebo si el pedido es para España y asigno unos gastos de envío distintos según el caso
        country = order_data.get('country')

        if country == 'Spain':
            order_data['shipping_cost'] = 6.00
        else:
            order_data['shipping_cost'] = 12.00

        # Serializo y grabo los datos del pedido
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_save = order_serializer.save()
            # recupero el ID del pedido insertado y lo guardo con cada línea del pedido
            id_order = order_save.id
            for line_data in order_lines_data:
                line_data['order'] = id_order
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Serializo y grabo los datos de las líneas del pedido
        order_lines_serializer = OrderLinesSerializer(data=order_lines_data, many=True)
        if order_lines_serializer.is_valid():
            order_lines_serializer.save()
        else:
            # Si falla al grabar las líneas del pedido, borro los datos del pedido insertado
            Order.objects.filter(id=order_serializer.data['id']).delete()
            return Response(order_lines_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


# Recuperar un pedido
class RecoverOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization", ))
    def dispatch(self, *args, **kwargs):
        return super(RecoverOrdersViewSet, self).dispatch(*args, **kwargs)

    # Obtengo las líneas del pedido que coincidan con su ID y preparo la respuesta
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Compruebo si el token existe y si coincide con el usuario asociado al pedido solicitado
        auth_token = request.auth
        if request.user.is_superuser:
            pass
        elif auth_token is None or auth_token.user_id != instance.user_id:
            raise exceptions.PermissionDenied("No tienes permisos para acceder a este recurso.")

        # Serializo la instancia del modelo Order
        order_serializer = self.get_serializer(instance)

        # Obtengo las líneas de pedido relacionadas con la instancia del modelo Order
        order_lines = OrderLines.objects.filter(order_id=instance.id)

        # Serializo las líneas de pedido
        order_lines_serializer = OrderLinesSerializer(order_lines, many=True)

        # Combino los datos serializados y preparo la respuesta
        data = {
            'pedido': order_serializer.data,
            'pedido_lineas': order_lines_serializer.data
        }

        return Response(data)


# Listar pedidos
class OrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization", ))
    def dispatch(self, *args, **kwargs):
        return super(OrdersViewSet, self).dispatch(*args, **kwargs)

    # Si es superuser devuelvo todas las líneas. Si es user devuelvo solo sus líneas.
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user_id=user.id)
