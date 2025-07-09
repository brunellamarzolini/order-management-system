from django.db import models
from core.models import BaseModel
from core.mixin_models import ModelDiffMixin
from localization.models import Language
from django.conf import settings

class Order(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    products = models.ManyToManyField('Product', related_name='orders')

    class Meta:
        ordering = ["-created_at"]
    
class Product(BaseModel, ModelDiffMixin):
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        try:
            return self.translations.get(lang__code=settings.DEFAULT_LANG).name
        except ProductLang.DoesNotExist:
            return str(self.pk)
        
    class Meta:
        ordering = ["created_at"]
    
class ProductLang(BaseModel):
    product = models.ForeignKey(Product, related_name='translations', on_delete=models.CASCADE)
    lang = models.ForeignKey(Language, models.CASCADE, related_name="+", default=settings.DEFAULT_LANG)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ["product", "lang"]

    def __str__(self):
        return self.name
    