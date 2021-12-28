from django.core.management.base import BaseCommand
from django.conf import settings
import os
class Command(BaseCommand):
    help = "Not yet"
    def add_arguments(self, parser):
      parser.add_argument('project-name') #type=int, default="something", help="helping text"
    def handle(self, *args, **options):
      lineNum = 0
      choice = ''
      projectName = options['project-name']
      os.system(f'pip install djangorestframework')
      os.system(f'pip install django-cors-headers')
      with open(f"{projectName}/settings.py", 'a+') as settingsFile:
        for line in settingsFile:
          lineNum +=1
        settingsFile.seek(lineNum)
        settingsFile.write(f"\nINSTALLED_APPS.append('rest_framework')\n")
        settingsFile.write(f"\nINSTALLED_APPS.append('corsheaders')\n")
        settingsFile.write(f"\nMIDDLEWARE.append('corsheaders.middleware.CorsMiddleware')\n")
        settingsFile.write("""\n
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
        \n""")

      choice = input("Do You Want To Make An App? (write the app name/n): ")
      appName = choice 
      if (choice != 'n' or choice != 'no'):
        os.system(f'python manage.py auto-app-drf {projectName} {appName}')
      else:
        choice = ''
      