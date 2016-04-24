import datetime
from datetime import datetime as DT
from django.http import HttpResponse
from django.shortcuts import render
from utilities.getdata import DataMap
from .models import WaterTemperature as WT
from .models import DischargeData as DD
from .models import GDD
from utilities.soap import SoapCalls
import pytz

def index(request):
    return render(request, 'kelp/index.html')

def populate_full_water_temperature(request):
    obj = SoapCalls()
    DataFormat = 'json'
    sensors = obj.GetSensors(DataFormat)

    sDate = DT(2016, 1, 1)
    eDate = sDate + datetime.timedelta(days=9)
    stationNumbers = get_station_num(sensors, 'WT')

    temperature_data = None
    count = 0

    while eDate < DT.today():
        count = count + 1
        print ("**** Writing batch: %s" % count)
        sDate = eDate + datetime.timedelta(days=1)
        eDate = eDate + datetime.timedelta(days=10)
        for x in stationNumbers:
            temperature_x = obj.GetTimeSeriesData(x, ['WT'], sDate.isoformat(), eDate.isoformat(), DataFormat)
            for x in temperature_x['TimeSeriesData']:
                wt_datetime = DT.strptime(x['TimeStamp'], '%m/%d/%Y %I:%M:%S %p')
                wt = WT(station_id=x['StationID'], station_name=x['StationName'],
                        timestamp=wt_datetime, value=x['Value'])
                wt.save()
    return HttpResponse('Written to database FULL')


def populate_curr_water_temperature(request):
    obj = SoapCalls()
    DataFormat = 'json'
    sensors = obj.GetSensors(DataFormat)

    dbObj = WT.objects.latest('timestamp')
    sDate = dbObj.timestamp + datetime.timedelta(minutes=5)

    eDate = datetime.datetime.today().isoformat().split('.')[0]
    stationNumbers = get_station_num(sensors, 'WT')

    temperature_data = None

    for x in stationNumbers:
        temperature_x = obj.GetTimeSeriesData(x, ['WT'], sDate.isoformat(), eDate, DataFormat)
        for x in temperature_x['TimeSeriesData']:
            wt_datetime = DT.strptime(x['TimeStamp'], '%m/%d/%Y %I:%M:%S %p')
            wt = WT(station_id=x['StationID'], station_name=x['StationName'],
                    timestamp=wt_datetime, value=x['Value'])
            wt.save()
    return HttpResponse('Written to database CURRENT')


def populate_full_discharge(request):
    obj = SoapCalls()
    DataFormat = 'json'
    sensors = obj.GetSensors(DataFormat)

    sDate = DT(2016, 1, 1)
    eDate = sDate + datetime.timedelta(days=2)
    stationNumbers = get_station_num(sensors, 'DISCHARGE')

    temperature_data = None
    count = 0

    while eDate < sDate + datetime.timedelta(days=4): #DT.today():
        count = count + 1
        print ("**** Writing batch: %s" % count)
        sDate = eDate + datetime.timedelta(days=1)
        eDate = eDate + datetime.timedelta(days=2)
        for x in stationNumbers:
            discharge_x = obj.GetTimeSeriesData(x, ['DISCHARGE'], sDate.isoformat(), eDate.isoformat(), DataFormat)
            for x in discharge_x['TimeSeriesData']:
                wt_datetime = DT.strptime(x['TimeStamp'], '%m/%d/%Y %I:%M:%S %p')
                wt = DD(station_id=x['StationID'], station_name=x['StationName'],
                        timestamp=wt_datetime, value=x['Value'])
                wt.save()
    return HttpResponse('Written to database FULL')

#
# def gdd_last_updated_date(request):
#     dm = DataMap()
#     dbObj = GDD.objects.latest('timestamp')
#     delta = DT.today() - dbObj.timestamp.isoformat()
#     if delta.days > 1:
#         print delta.days
#         #jsonObj = dm.calculate_GDD(dbObj.timestamp.isoformat())
#     return HttpResponse('Fetch last updated date - GDD')

def get_station_num(sensors, sensorName):
    sensordata = filter(lambda x: x['SensorName'] in ['%s' % (sensorName)], sensors['Sensors'])
    stationNumbers = map(lambda x: x['StationNumber'], sensordata)
    return stationNumbers

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
