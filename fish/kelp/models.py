from __future__ import unicode_literals

from django.db import models

class WaterTemperature(models.Model):
    station_id = models.CharField(max_length=100)
    station_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    value = models.FloatField()


class DischargeData(models.Model):
    station_id = models.CharField(max_length=100)
    station_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    velocity = models.FloatField(default=0)

class SpawningStreamLength(models.Model):
    incubation_time = models.FloatField()
    stream_length = models.FloatField()
    actual_length = models.FloatField()
    station_id = models.CharField(max_length=100)
    station_name = models.CharField(max_length=200)

class GDD(models.Model):
    gdd = models.FloatField()
    timestamp = models.DateTimeField()
    spawning_likelihood = models.CharField(max_length=100)
    