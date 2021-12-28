from django.core.management.base import BaseCommand
from django.conf import settings
import os
class Command(BaseCommand):
    help = "Not yet"
    def add_arguments(self, parser):
      parser.add_argument('app-name') #type=int, default="something", help="helping text"
    def handle(self, *args, **options):
      appName = options['app-name']
      lineNum = 0
      models = {}
      modelFields = {}
      modelNum = int(input("How Many Models?: "))
      with open(f"{appName}/models.py", 'a+') as modelsFile:
        while(0 < modelNum):
          modelName = input(f"Model {modelNum} Name: ")
          models[f'{modelName}'] = 1
          modelNum -=1
        modelFieldsNum = int(input(f"How Many Fields? (For All models): "))          
        while(0 < modelFieldsNum):
          modelFieldName = input(f"Model Field {modelFieldsNum} Name: ")
          modelFieldType = input(f"Field {modelFieldName} Type (Integer, Char, Decimal, etc..): ")
          modelFields[f'{modelFieldName}'] = modelFieldType
          modelFieldsNum -=1
        for line in modelsFile:
          lineNum +=1
        modelsFile.seek(lineNum)
        for key in models:
          modelsFile.write(f'\nclass {key}(models.Model):\n')
          for key, value in modelFields.items():
            modelsFile.write(f'   {key} = models.{value}Field(max_length=100)\n')

        self.stdout.write(self.style.SUCCESS(f'Successfully created all models in {appName}/models.py file'))
      choice = input("Want to Make views [Basic CRUD] for the models? [This will also create a serializers and a urls file] (y/n): ")
      if(choice == 'y' or choice == 'yes'):
        with open(f"{appName}/serializers.py", 'a+') as serializersFile:
          self.stdout.write(self.style.SUCCESS(f'Created {appName}/serializers.py file Successfully!'))
          serializersFile.write(f'\nfrom rest_framework import serializers\n')
          serializersFile.write(f'\nfrom . import models\n')
          for key in models:
            serializersFile.write(f'''\n
class {key}Serializer(serializers.ModelSerializer):

  class Meta:
    model = models.{key}
    fields = '__all__'
                                  \n''')
        with open(f"{appName}/views.py", 'a+') as viewsFile:      
          viewsFile.seek(0)
          viewsFile.write(f'\nfrom . import models\n')
          viewsFile.write(f'\nfrom . import serializers\n')
          viewsFile.write(f'\nfrom rest_framework.decorators import api_view,permission_classes\n')
          viewsFile.write(f'\nfrom rest_framework.response import Response\n')
          for line in viewsFile:
            lineNum +=1
          viewsFile.seek(lineNum)
          for key in models:
            viewsFile.write(f'\n#----------------------------------------------\n')
            viewsFile.write(f'\n#GET ALL {key}s\n')
            viewsFile.write(f"""    
@api_view(['GET'])
def {key}sIndex(request):
    All{key}s = models.{key}.objects.all()
    serializer = serializers.{key}Serializer(All{key}s, many=True)
    data = {{'data':serializer.data}}
    return Response(data)
            
                            \n""")
            viewsFile.write(f'\n#------------------\n')
            viewsFile.write(f'\n#GET GROUP OF {key}s\n')
            viewsFile.write(f'''\n        
@api_view(['GET'])
def {key}sList(request, name):
    {key}sGroup = models.{key}.objects.filter(name=name)
    serializer = serializers.{key}Serializer({key}sGroup, many=True)
    data = {{'data':serializer.data}}
    return Response(data)
            
                            \n''')
            viewsFile.write(f'\n#------------------\n')
            viewsFile.write(f'\n#GET ONE {key}\n')
            viewsFile.write(f'''\n        
@api_view(['GET'])
def Get{key}(request, id):
    One{key} = models.{key}.objects.get(id=id)
    serializer = serializers.{key}Serializer(One{key}, many=False)
    data = {{'data':serializer.data}}
    return Response(data)
            
                            \n''')
            viewsFile.write(f'\n#------------------\n')
            viewsFile.write(f'\n#CREATE A {key}\n')
            viewsFile.write(f'''\n        
@api_view(['POST'])
def Create{key}(request):
  serializer = serializers.{key}Serializer(data=''')
            viewsFile.write('{\n')
            for Fieldkey in modelFields:
              viewsFile.write(f'''      
'{Fieldkey}': request.data['{Fieldkey}'],
  \n''')
            viewsFile.write('})')
            viewsFile.write(f'''\n 
  if serializer.is_valid():
    serializer.save()
  data = {{'data':serializer.data}}
  return Response(data)
                            \n''')
            
            viewsFile.write(f'\n#------------------\n')
            viewsFile.write(f'\n#UPDATE A {key}\n')
            viewsFile.write(f'''\n        
@api_view(['PUT'])
def Update{key}(request,id):
  One{key} = models.{key}.objects.get(id=id)
  serializer = serializers.{key}Serializer(instance=One{key},data=''')
            viewsFile.write('{\n')
            for Fieldkey in modelFields:
              viewsFile.write(f'''      
'{Fieldkey}': request.data['{Fieldkey}'],
  \n''')
            viewsFile.write('})')
            viewsFile.write(f'''\n 
  if serializer.is_valid():
    serializer.save()
  data = {{'data':serializer.data}}
  return Response(data)
                            \n''')
            
            viewsFile.write(f'\n#------------------\n')
            viewsFile.write(f'\n#DELETE A {key}\n')
            viewsFile.write(f'''\n        
@api_view(['DELETE'])
def Delete{key}(request,id):
    One{key} = models.{key}.objects.get(id=id)
    One{key}.delete()
    return Response(True)
                            \n''')
            
            viewsFile.write(f'\n#------------------\n')
            viewsFile.write(f'\n#---------------------------------------------\n')
            with open(f"{appName}/urls.py", 'a+') as appUrlsFile:
              appUrlsFile.seek(0)
              appUrlsFile.write(f"\nfrom . import views\n")

              for line in appUrlsFile:
                lineNum +=1
                appUrlsFile.seek(lineNum)
              
              appUrlsFile.write(f"\nfrom django.urls import path\n")
              appUrlsFile.write(f"\nurlpatterns = []\n")
              appUrlsFile.write(f"\nurlpatterns.append(path('{key}sIndex/', views.{key}sIndex))\n")
              appUrlsFile.write(f"\nurlpatterns.append(path('{key}sList/<str:name>/', views.{key}sList))\n")
              appUrlsFile.write(f"\nurlpatterns.append(path('Get{key}/<int:id>', views.Get{key}))\n")
              appUrlsFile.write(f"\nurlpatterns.append(path('Create{key}/', views.Create{key}))\n")
              appUrlsFile.write(f"\nurlpatterns.append(path('Update{key}/<int:id>/', views.Update{key}))\n")
              appUrlsFile.write(f"\nurlpatterns.append(path('Delete{key}/<int:id>/', views.Delete{key}))\n")
            with open(f"{appName}/admin.py", 'a+') as adminFile:
              adminFile.seek(0)
              adminFile.write("\nfrom . import models\n")
              for line in adminFile:
                lineNum +=1
                adminFile.seek(lineNum)
              adminFile.write(f"admin.site.register(models.{key})")
        self.stdout.write(self.style.SUCCESS(f'Created {appName}/urls.py file Successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created all the CRUD functions on {appName}/views.py'))
      else:
        choice = ''
      