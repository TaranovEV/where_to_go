from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from places.models import *


def show_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    data = {
        'title': place.title,
        'imgs': [images.image.url for images in place.imgs.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        }
    }

    return JsonResponse(data,
                        safe=False,
                        json_dumps_params={
                            'ensure_ascii': False,
                            'indent': 2
                        })


def show_index(request):
    features = []
    places = Place.objects.all()
    for place in places:
        coordinates = [place.lng, place.lat]
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': coordinates
            },
            'properties': {
                'title': place.title,
                'placeId': place.placeId,
                'detailsUrl': reverse('place-geojson', args=[place.id])
            }
        })
    data = {
      'type': 'FeatureCollection',
      'features': features
    }
    return render(request,
                  'index.html',
                  context={'title_company_json': data})
