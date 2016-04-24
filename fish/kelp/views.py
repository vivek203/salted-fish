from django.http import HttpResponse
from django.shortcuts import render
from utilities.getdata import DataMap
from .models import WaterTemperature
from datetime import datetime
import pytz

def index(request):
    return render(request, 'kelp/index.html')

def populate_water_temperature(request):
    dm = DataMap()
    # print (dm.sensors)
    sensordata = filter(lambda x: x['SensorName'] in ['WT'], dm.sensors['Sensors'])
    sensornames = map(lambda x: x['StationNumber'], sensordata)
    # print (sensornames)
    small_json = dm.get_water_temp_data()

    for x in small_json['TimeSeriesData']:
        wt_datetime = datetime.strptime(x['TimeStamp'], '%m/%d/%Y %I:%M:%S %p')
        wt = WaterTemperature(station_id=x['StationID'], station_name=x['StationName'],
                              timestamp=wt_datetime, value=x['Value'])
        wt.save()

    return HttpResponse('Written to database')
    # return HttpResponse(str(small_json))
    # return HttpResponse('boooo')
