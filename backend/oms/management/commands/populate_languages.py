import json
from django.core.management.base import BaseCommand
from localization.models import Language
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with languages from JSON file.'

    def handle(self, *args, **options):
        path = settings.BASE_DIR / 'oms' / 'data' / 'languages.json'
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            obj, created = Language.objects.get_or_create(code=entry['code'], defaults={'name': entry['name']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added language: {obj.name}"))
            else:
                self.stdout.write(f"Language already exists: {obj.name}")
