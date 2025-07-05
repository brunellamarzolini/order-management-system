from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Order, Product, ProductLang

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date",)
    search_fields = ("name", "description",)
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }
    filter_horizontal = ('products',)

admin.site.register(Order, OrderAdmin)

class ProductLangInline(admin.TabularInline):
    model = ProductLang
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "price")
    inlines = [ProductLangInline] 

admin.site.register(Product, ProductAdmin)