from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.core.cache import cache
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, OrderListSerializer
from .filters import OrderFilter
from .mixin_views import CacheDetailResponseMixin, CacheListResponseMixin

# Create your views here.
class ProductViewSet(CacheListResponseMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["id", "translations__name"]

class OrderViewSet(CacheDetailResponseMixin, CacheListResponseMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related('products').annotate(
        total_amount_db=Sum('products__price')
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return super().get_serializer_class()
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["id", "name", "description"]
    filterset_class = OrderFilter
    ordering_fields = ["created_at", "total_amount_db"]
    ordering = ["created_at"]


# class ProductOrderViewSet(ListModelMixin, GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProductSerializer
#     def get_queryset(self):
#         order_pk = self.kwargs['pk']
#         order = get_object_or_404(Order, pk=order_pk)
#         qs = order.products.prefetch_related('translations').all()
#         return qs
# 
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["translations__name"]
#     ordering_fields = ["price"]
#     ordering = ["id"]
