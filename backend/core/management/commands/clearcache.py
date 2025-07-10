from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clears all caches.'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('All caches have been cleared.'))
