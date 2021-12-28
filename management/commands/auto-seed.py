from django.core.management.base import BaseCommand
from django.conf import settings
import os
class Command(BaseCommand):
    help = "Not yet"
    def add_arguments(self, parser):
      parser.add_argument('project-name') #type=int, default="something", help="helping text"
      parser.add_argument('app-name') #type=int, default="something", help="helping text"
    def handle(self, *args, **options):
      pass
      