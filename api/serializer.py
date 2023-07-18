from rest_framework import serializers
from .models import Product, Order, OrderLines


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLines
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
