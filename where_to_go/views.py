from django.shortcuts import render
from places.models import *


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
                'detailsUrl': f'static/places/{place.placeId}.json'
            }
        })
    data = {
      'type': 'FeatureCollection',
      'features': features
    }

    return render(request,
                  'index.html',
                  context={'title_company_json': data})
