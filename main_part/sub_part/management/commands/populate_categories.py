from sub_part.models  import *
from django.core.management.base import BaseCommand
from typing import Any


class Command(BaseCommand):
    help="this command is  inserts category data"

    def handle(self, *args:Any, **options:Any):
        #delete existing data becoz create slug 
        category.objects.all().delete()

        category_name=["sport","technology","science","art","Engineering"]
     
        for categories in category_name:
            category.objects.create(name=categories)

        self.stdout.write(self.style.SUCCESS("completed insert data"))

 