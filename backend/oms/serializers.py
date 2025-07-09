from rest_framework import serializers
from localization.fields import TranslatedField
from oms.models import Order, Product, ProductLang

class ProductLangSerializer(serializers.ModelSerializer):

    lang_code = serializers.CharField(source='lang.code')

    class Meta:
        model = ProductLang
        fields = ["lang_code", "name"]


class ProductSerializer(serializers.ModelSerializer):

    name = TranslatedField("name")

    class Meta:
        model = Product
        fields = ["id", "name", "translations", "price"]


class BaseOrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "name", "description", "total_amount", "created_at", "updated_at"
        ]

    def get_total_amount(self, obj):
        return getattr(obj, 'total_amount_db', None) or sum(product.price for product in obj.products.all())

class OrderListSerializer(BaseOrderSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(BaseOrderSerializer.Meta):
        fields = BaseOrderSerializer.Meta.fields + ["products"]

class OrderSerializer(BaseOrderSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all(), write_only=True
    )
    product_details = ProductSerializer(source='products', many=True, read_only=True)

    class Meta(BaseOrderSerializer.Meta):
        fields = BaseOrderSerializer.Meta.fields + ["products", "product_details"]