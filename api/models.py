from django.db import models
# Para implementar el sistema de autenticación por token
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.

# Productos
class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    color = models.CharField(max_length=30)
    cost = models.DecimalField(max_digits=7, decimal_places=2)


# Pedidos
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    order_date = models.DateField(auto_now_add=True)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Order {self.pk}"


# Líneas del pedido
class OrderLines(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    sell_cost = models.DecimalField(max_digits=7, decimal_places=2)


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40)


# Genero tokens para los nuevos usuarios
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)