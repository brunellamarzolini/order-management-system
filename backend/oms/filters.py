import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")
    created_at_exact = django_filters.DateFilter(field_name="created_at", lookup_expr="exact")

    class Meta:
        model = Order
        fields = ["created_at", "created_at_exact"]
