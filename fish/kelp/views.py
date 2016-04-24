from django.http import HttpResponse
from django.shortcuts import render
from utilities.getdata import DataMap
from .models import WaterTemperature as WT
from datetime import datetime
import pytz

def index(request):
    return render(request, 'kelp/index.html')

def populate_water_temperature(request):
    dm = DataMap()
    small_json = dm.get_water_temp_data_FULL()

    for x in small_json['TimeSeriesData']:
        wt_datetime = datetime.strptime(x['TimeStamp'], '%m/%d/%Y %I:%M:%S %p')
        wt = WT(station_id=x['StationID'], station_name=x['StationName'],
                timestamp=wt_datetime, value=x['Value'])
        wt.save()

    return HttpResponse('Written to database')

def populate_current_water_temperature(request):
    dm = DataMap()
    dbObj = WT.objects.latest('timestamp')
    jsonObj = dm.get_water_temp_data(dbObj.timestamp.isoformat())

    for x in jsonObj['TimeSeriesData']:
        wt_datetime = datetime.strptime(x['TimeStamp'], '%m/%d/%Y %I:%M:%S %p')
        wt = WT(station_id=x['StationID'], station_name=x['StationName'],
                timestamp=wt_datetime, value=x['Value'])
        wt.save()

    return HttpResponse('Written to database')
