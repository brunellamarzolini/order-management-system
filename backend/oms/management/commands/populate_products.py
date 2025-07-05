import json
from django.core.management.base import BaseCommand
from oms.models import Product, ProductLang, Language
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with products and translations from JSON file.'

    def handle(self, *args, **options):
        path = settings.BASE_DIR / 'oms' / 'data' / 'products.json'
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            product, created = Product.objects.get_or_create(price=entry['price'])
            for trans in entry.get('translations', []):
                lang = Language.objects.get(code=trans['lang'])
                ProductLang.objects.get_or_create(product=product, lang=lang, defaults={'name': trans['name']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added product with translations: {product.pk}"))
            else:
                self.stdout.write(f"Product already exists: {product.pk}")
