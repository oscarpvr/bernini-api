from django.urls import path, include
from rest_framework import routers
from api import views



router = routers.DefaultRouter()
router.register(r'products', views.ProductsViewSet, basename='products')
router.register(r'create_orders', views.CreateOrdersViewSet, basename='create_orders')
router.register(r'recover_orders', views.RecoverOrdersViewSet, basename='recover_orders')
router.register(r'orders', views.OrdersViewSet, basename='orders')



urlpatterns = [
    path('', include(router.urls))
]
