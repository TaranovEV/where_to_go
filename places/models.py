from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название')
    place_id = models.CharField(max_length=200,
                               verbose_name='Id',
                               unique=True)
    description_short = models.TextField(verbose_name='Краткое описание',
                                         blank=True)
    description_long = HTMLField(verbose_name='Полное описание',
                                         blank=True)
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place,
                              related_name='imgs',
                              on_delete=models.CASCADE)
    image_number = (
        models.PositiveSmallIntegerField(verbose_name='Номер изображения',
                                         default=1)
    )
    image = models.ImageField(verbose_name='Изображение')

    class Meta(object):
        ordering = ['image_number']

    def __str__(self):
        return '{} {}'.format(self.image_number, self.place)
