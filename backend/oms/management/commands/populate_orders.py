import json
from django.core.management.base import BaseCommand
from oms.models import Order, Product, ProductLang
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with orders from JSON file.'

    def handle(self, *args, **options):
        path = settings.BASE_DIR / 'oms' / 'data' / 'orders.json'
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            order, created = Order.objects.get_or_create(
                name=entry['name'],
                defaults={
                    'description': entry.get('description', ''),
                    'date': entry['date']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added order: {order.name}"))
            else:
                self.stdout.write(f"Order already exists: {order.name}")
            # Add products to order by matching ProductLang name (English)
            for prod_name in entry['products']:
                product_lang = ProductLang.objects.filter(name=prod_name, lang__code='en').first()
                if product_lang:
                    order.products.add(product_lang.product)
                else:
                    self.stdout.write(self.style.WARNING(f"Product not found for name: {prod_name}"))
