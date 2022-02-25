from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from places.models import Place


def show_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    place_fields = {
        'title': place.title,
        'imgs': [images.image.url for images in place.imgs.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        }
    }

    return JsonResponse(place_fields,
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
                'placeId': place.place_id,
                'detailsUrl': reverse('place-geojson', args=[place.id])
            }
        })
    places_with_atributes = {
      'type': 'FeatureCollection',
      'features': features
    }
    return render(request,
                  'index.html',
                  context={'places_with_atributes': places_with_atributes})
