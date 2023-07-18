from django.contrib import admin
from .models import Product, Order, OrderLines

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderLines)