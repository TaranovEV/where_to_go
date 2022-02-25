import os
import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from places.models import Place, Image



def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

class Command(BaseCommand):
    help = 'Add place in DB'

    def add_arguments(self, parser):
        parser.add_argument('json',
                        help='''url адрес файла JSON''',
                        type=str,)

    def handle(self, *args, **options):
        response = requests.get(options.get('json'))
        check_for_redirect(response)
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
            filename = os.path.basename(image_url)
            image_response = requests.get(image_url)
            check_for_redirect(image_response)
            image_response.raise_for_status()
            obj, created = Image.objects.get_or_create(title=place,
                                                       image_number=image_number)
            obj.image.save(filename, ContentFile(image_response.content))
            obj.save()