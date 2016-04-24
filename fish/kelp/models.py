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
