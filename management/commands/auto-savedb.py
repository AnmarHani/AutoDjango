from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
      os.system(f'python manage.py makemigrations')
      os.system(f'python manage.py migrate')
      os.system(f'python manage.py runserver')
      