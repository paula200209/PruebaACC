from django.db import models
from .utils import get_country_coordinates

class Movie(models.Model):
    titulo = models.CharField(max_length=255)
    calificacion = models.IntegerField()
    pais = models.CharField(max_length=100)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.pk:  # OJO: Solo actualiza las coordenadas si es una nueva instancia
            coords = get_country_coordinates(self.pais)
            if coords:
                self.longitude, self.latitude = coords
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class CountryCoordinates(models.Model):
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.country
