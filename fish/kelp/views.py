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

def calc_gdd(request):
	wt_objects = WT.objects.all()
	day_dict = {}
	for wt_o in wt_objects:
		# logic: sum every value that are in the same day
		# check if sum > 15, if yes, add to global_sum
		key_code = wt_o.timestamp.day + wt_o.timestamp.month + wt_o.timestamp.year
		if key_code in day_dict:
			day_dict[key_code] += wt_o.value
		else:
			day_dict[key_code] = wt_o.value

	gdd = 0
	for key, sum_val in day_dict.items():
		if sum_val > 15 :
			gdd += sum_val
	
	return HttpResponse(gdd)
