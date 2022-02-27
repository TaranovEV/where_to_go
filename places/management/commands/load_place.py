import os
import requests
from urllib.parse import urlsplit, unquote
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
        response = requests.get(options.get('json'))
        response.raise_for_status()
        place_from_url = response.json()
        place, created = Place.objects.get_or_create(
            title = place_from_url['title'],
            placeId = place_from_url['title'],
            lng = place_from_url['coordinates']['lng'],
            lat = place_from_url['coordinates']['lat'],
            defaults={
                'description_short': '',
                'description_long': '',},
        )
        for image_number, image_url in enumerate(place_from_url['imgs'], 1):
            path, filename = (
                os.path.split(unquote(urlsplit(image_url).path))
            )
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            place_image, created = Image.objects.get_or_create(title=place,
                                                       image_number=image_number)
            place_image.image.save(filename, ContentFile(image_response.content))