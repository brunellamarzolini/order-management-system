from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
#router.register(r'orders/(?P<pk>[\w-]+)/products', ProductOrderViewSet, basename='order-products')


urlpatterns = [
    path('', include(router.urls)),
]
