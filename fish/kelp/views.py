import datetime
from datetime import datetime as DT
from django.http import HttpResponse
from django.shortcuts import render
from utilities.getdata import DataMap
from .models import WaterTemperature as WT
<<<<<<< Updated upstream
from .models import DischargeData as DD
from .models import GDD
from .models import SpawningStreamLength as SPWN
from .models import DailyWaterTemperature as DWT
from utilities.soap import SoapCalls
import pytz
import numpy as np
=======
import datetime
import pytz
import csv
>>>>>>> Stashed changes

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
                try:
                    wt = WT(station_id=x['StationID'], station_name=x['StationName'],
                            timestamp=wt_datetime, value=x['Value'])
                    wt.save()
                except Exception:
                    continue

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
            try:
                wt = WT(station_id=x['StationID'], station_name=x['StationName'],
                    timestamp=wt_datetime, value=x['Value'])
                wt.save()
            except Exception:
                continue
    return HttpResponse('Written to database CURRENT')


def populate_full_discharge(request):
    obj = SoapCalls()
    DataFormat = 'json'

    sDate = DT(2016, 1, 1)

    temperature_data = None
    count = 0

    data = np.random.uniform(0, 4, 115)
    data = np.around(data, 1)
    data = data.tolist()

    i = -1
    while sDate < DT.today():
        count = count + 1
        print ("**** Writing discharge batch: %s" % count)
        i = i + 1
        date = sDate
        sDate = sDate + datetime.timedelta(days=1)
        print i
        vel = (0.2692 * data[i]) + 0.0984
        try:
            dObj = DD(station_id='HY040', station_name='KROSNO CR',
                timestamp=date, value=data[i], velocity=vel)
            dObj.save()
        except Exception:
            continue
    return HttpResponse('Written to discharge database FULL')

def populate_discharge(request):
    obj = SoapCalls()
    DataFormat = 'json'

    dbObj = DD.objects.latest('timestamp')
    sDate = DT.combine(datetime.date.today(), datetime.time.min)

    temperature_data = None
    count = 0

    data = np.random.uniform(0, 4, 1)
    data = np.around(data, 1)
    data = data.tolist()
    vel = 0.2692 * data[0] + 0.0984
    try:
        dObj = DD(station_id='HY040', station_name='KROSNO CR',
                timestamp=sDate, value=data[0], velocity=vel)
        dObj.save()
    except Exception:
        pass
    return HttpResponse('Written to discharge database FULL')

def get_station_num(sensors, sensorName):
    sensordata = filter(lambda x: x['SensorName'] in ['%s' % (sensorName)], sensors['Sensors'])
    stationNumbers = map(lambda x: x['StationNumber'], sensordata)
    return stationNumbers


def populate_gdd_full(request):
    dwt_objects = DWT.objects.all()
    gddsum = 0
    count = 0
    for dwt_o in dwt_objects:
        count = count + 1
        print ("**** Writing GDD batch: %s" % count)
        if dwt_o.value > 15:
            gddsum += dwt_o.value
            print 'updated gdd'
        try:
            dObj = GDD(gdd=np.around(gddsum, 1), timestamp=dwt_o.timestamp, spawning_likelihood='Not Suitable')
            dObj.save()
        except Exception:
            continue
    return HttpResponse('Written to GDD database FULL')

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

def get_temperature_csv(request):
    response = HttpResponse(content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['date', 'temperature'])

    temps = WT.objects.filter(station_id='HY040', timestamp__lte=datetime.datetime.today(), timestamp__gt=datetime.datetime.today()-datetime.timedelta(days=15))
    for temp in temps:
        writer.writerow([temp.timestamp, temp.value])
    # writer.writerow(['1', '5'])
    # writer.writerow(['2', '10'])
    # writer.writerow(['3', '15'])

    return response
