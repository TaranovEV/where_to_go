from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название')
    placeId = models.CharField(max_length=200,
                               verbose_name='Id')
    description_short = models.CharField(max_length=300,
                                         verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    def __str__(self):
        return '{}'.format(self.title)


class Image(models.Model):
    title = models.ForeignKey(Place,
                              related_name='imgs',
                              null=True,
                              on_delete=models.SET_NULL)
    image_number = (
        models.PositiveSmallIntegerField(verbose_name='Номер изображения')
    )
    image = models.ImageField(verbose_name='Изображение')

    def __str__(self):
        return '{} {}'.format(self.image_number, self.title)
