import os
import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from places.models import Place, Image


class Command(BaseCommand):
    help = 'Add place in DB'

    def add_arguments(self, parser):
        parser.add_argument('json',
                        help='''url адрес файла JSON''',
                        type=str,)

    def handle(self, *args, **options):
        response = requests.get(options.get('json')).json()
        place, created = Place.objects.get_or_create(
            title = response['title'],
            placeId = response['title'],
            description_short = response['description_short'],
            description_long = response['description_long'],
            lng = response['coordinates']['lng'],
            lat = response['coordinates']['lat'],
        )
        iter = 1
        for image_url in response['imgs']:
            filename = os.path.basename(image_url)
            image_response = requests.get(image_url)
            obj, created = Image.objects.get_or_create(title=place, image_number=iter)
            obj.image.save(filename, ContentFile(image_response.content))
            obj.save()
            iter+=1