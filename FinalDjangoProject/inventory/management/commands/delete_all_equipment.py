from django.core.management.base import BaseCommand
from inventory.models import Equipment

class Command(BaseCommand):
    help = 'Deletes all items from the Equipment model'

    def handle(self, *args, **options):
        Equipment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all items from the Equipment model.'))