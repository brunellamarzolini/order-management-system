from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Order, ProductLang
from localization.models import Language

def get_supported_languages():
    return Language.objects.values_list('code', flat=True)

def delete_product_cache(product_id=None):
    for lang in get_supported_languages():
        cache.delete_pattern(f'product:list:{lang}*')
        if product_id:
            cache.delete(f'product:detail:{product_id}:{lang}')

def invalidate_related_order_details(product):
    related_orders = Order.objects.filter(products=product).values_list('pk', flat=True)
    for order_id in related_orders:
        for lang in get_supported_languages():
            cache.delete(f'order:detail:{order_id}:{lang}')

def delete_order_cache(order_id=None):
    for lang in get_supported_languages():
        cache.delete_pattern(f'order:list:{lang}*')
        
        if order_id:
            cache.delete(f'order:detail:{order_id}:{lang}')


@receiver([post_save, post_delete], sender=Product, dispatch_uid='invalidate_cache_by_product')
def product_cache_invalidation(sender, instance, raw=False, **kwargs):
    delete_product_cache(instance.pk)
    #invalidate_related_order_details(instance)

    if not raw:
        if instance.price:
            is_new = instance._state.adding
            if is_new or 'price' in instance.get_changed_fields():
                delete_order_cache() # I need this because i have total amount in order list


@receiver([post_save, post_delete], sender=ProductLang, dispatch_uid='invalidate_cache_by_product_lang')
def productlang_cache_invalidation(sender, instance, **kwargs):
    delete_product_cache(instance.product_id)
    invalidate_related_order_details(instance.product)

@receiver([post_save, post_delete], sender=Order, dispatch_uid='invalidate_cache_by_order')
def order_cache_invalidation(sender, instance, **kwargs):
    delete_order_cache(instance.pk)