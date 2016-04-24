import datetime
from soap import SoapCalls
from pprint import pformat
from pandas.io.json import json_normalize
from jsonmerge import merge

class DataMap(object):

    def __init__(self):
        self.obj = SoapCalls()
        self.DataFormat='json'
        self.sensors = self.obj.GetSensors(self.DataFormat)

    def get_daily_discharge(self):
        sDate = datetime.datetime(2016, 1, 1)
        eDate = sDate + datetime.timedelta(days=9)
        stationNumbers = self.get_station_num('DISCHARGE')
        while eDate < datetime.datetime(2016, 1, 30):
            sDate = eDate + datetime.timedelta(days=1)
            eDate = eDate + datetime.timedelta(days=10)
            discharge_data = None
            for x in stationNumbers:
                # discharge_x = self.obj.GetTimeSeriesData(x, ['DISCHARGE'], sDate.isoformat(),
                #                                         eDate.isoformat(), self.DataFormat)
                # discharge_data = merge(discharge_data, discharge_x)
                print x
        return discharge_data

    def get_water_temp_data(self, sDate):
        eDate = datetime.datetime.today().isoformat().split('.')[0]
        stationNumbers = self.get_station_num('WT')
        temperature_data = None
        for x in stationNumbers:
            temperature_x = self.obj.GetTimeSeriesData(x, ['WT'], sDate,
                                                eDate, self.DataFormat)
            temperature_data = merge(temperature_data, temperature_x)
        return temperature_data


    def get_daily_discharge_FULL(self):
        sDate = datetime.datetime(2016, 1, 1)
        eDate = sDate + datetime.timedelta(days=9)
        stationNumbers = self.get_station_num('DISCHARGE')
        while eDate < datetime.datetime(2016, 1, 30):
            sDate = eDate + datetime.timedelta(days=1)
            eDate = eDate + datetime.timedelta(days=10)
            discharge_data = None
            for x in stationNumbers:
                # discharge_x = self.obj.GetTimeSeriesData(x, ['DISCHARGE'], sDate.isoformat(),
                #                                         eDate.isoformat(), self.DataFormat)
                # discharge_data = merge(discharge_data, discharge_x)
                print x
        return discharge_data

    def get_water_temp_data_FULL(self):
        sDate = datetime.datetime(2016, 1, 1)
        eDate = sDate + datetime.timedelta(days=9)
        stationNumbers = self.get_station_num('WT')
        temperature_data = None
        count=0
        while eDate < datetime.datetime.today():
            count = count+1
            print ("**** Writing batch: %s" % count)
            sDate = eDate + datetime.timedelta(days=1)
            eDate = eDate + datetime.timedelta(days=10)
            for x in stationNumbers:
                temperature_x = self.obj.GetTimeSeriesData(x, ['WT'], sDate.isoformat(),
                                                           eDate.isoformat(), self.DataFormat)
                temperature_data = merge(temperature_data, temperature_x)
        return temperature_data

    def get_station_num(self, sensorName):
        sensordata = filter(lambda x: x['SensorName'] in ['%s' % (sensorName)], self.sensors['Sensors'])
        stationNumbers = map(lambda x: x['StationNumber'], sensordata)
        return stationNumbers
#
# dm = DataMap()
# print (dm.sensors)
# sensordata = filter(lambda x: x['SensorName'] in ['WT'], dm.sensors['Sensors'])
# sensornames = map(lambda x: x['StationNumber'], sensordata)
# print pformat(sensornames)
# small_json = dm.get_water_temp_data()

# print pformat(dm.get_daily_discharge())