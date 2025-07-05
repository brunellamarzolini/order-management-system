from rest_framework import serializers
from localization.fields import TranslatedField
from oms.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    name = TranslatedField("name")

    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "name", "description", "date", "products", "total_amount"]

    def get_products(self, obj):
        request = self.context.get('request')
        if request and request.parser_context and request.parser_context.get('kwargs', {}).get('pk'):
            # Detail view: return full product objects
            return ProductSerializer(obj.products.all(), many=True, context=self.context).data
        
        # List view: return only product IDs
        return list(obj.products.values_list('id', flat=True))

    def get_total_amount(self, obj):
        return getattr(obj, 'total_amount_db', None) or sum(product.price for product in obj.products.all())