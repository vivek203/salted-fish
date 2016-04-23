from soap import SoapCalls
from pprint import pformat
from datetime import datetime

from pandas.io.json import json_normalize

import datetime

DataFormat='json'
obj = SoapCalls()
print pformat(obj.GetAllLocations(DataFormat))
data2 = obj.GetAllLocations(DataFormat)
print json_normalize(data2['Locations'], ['Elevation'])
data = obj.GetSensors('HY006', DataFormat)
print data
sensors = filter(lambda x: x['SensorName'] in ['WT'], data['Sensors'])

# print sensors
nrm = json_normalize(data['Sensors'])
print type(nrm)
str_date = '02/01/2016'
# print datetime.datetime.strptime(str_date, '%m/%d/%Y').date().isoformat()

sDate = datetime.date(2016, 1, 1).isoformat()
eDate = datetime.date(2016, 1, 5).isoformat()

# obj.GetTimeSeriesData('HY006', 'WT', '2016-01-01T10:20:15', '2016-01-05T10:20:15')
# obj.GetTimeSeriesData('HY006', 'WT', sDate, eDate)
# for x in sensors:
#     print obj.GetTimeSeriesData(x['StationNumber'], x['SensorName'], '1/1/2016', '1/5/2016')


# for x in sensors:
#     print pformat(obj.GetTimeSeriesData(x['StationNumber'], x['SensorName'], sDate, eDate))
