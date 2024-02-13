from django.core.management.base import BaseCommand  #type: ignore
from catalog.models import Product
from django.core.management import call_command #type: ignore

class Command(BaseCommand):
    help = 'Fill the database with new data and delete old data'

    def handle(self, *args, **options):
        # Удаление старых данных
        self.stdout.write(self.style.SUCCESS('Deleting old data...'))
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old data deleted successfully'))

        # Заполнение базы данных новыми данными
        self.stdout.write(self.style.SUCCESS('Filling the database with new data...'))
        call_command('loaddata', 'data_load.json')
        self.stdout.write(self.style.SUCCESS('New data added successfully'))
