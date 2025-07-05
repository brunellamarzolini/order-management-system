from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django.db.models import Sum, F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.orders.exists():
            raise ValidationError("Cannot delete product: it is associated with one or more orders.")
        return super().destroy(request, *args, **kwargs)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().annotate(
        total_amount_db=Sum('products__price')
    )
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["id", "name", "description"]
    filterset_fields = ["date"]
    ordering_fields = ["date", "total_amount_db"]
    ordering = ["date"]
