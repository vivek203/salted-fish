import json
from suds import WebFault
from suds.client import Client


class SoapCalls:
    def __init__(self):
        try:
            self.interface = 'http://trcagauging.ca/dataapi/trcagaugingAPI.asmx?wsdl'
            self.client = Client(self.interface)
        except WebFault, f:
            print f.fault

    def GetAllLocations(self, DataFormat):
        jsonData = self.client.service.GetAllLocations(DataFormat)
        return json.loads(jsonData)

    def GetAllLocationsInformation(self, DataFormat):
        jsonData = self.client.service.GetAllLocationsInformation(DataFormat)
        return json.loads(jsonData)

    def GetSensors(self, StationID, DataFormat):
        jsonData = self.client.service.GetSensors(StationID, DataFormat)
        return json.loads(jsonData)

    def GetTimeSeriesData(self, StationID, SensorName, sDate, eDate, DataFormat):
        jsonData = self.client.service.GetTimeSeriesData(StationID, SensorName, sDate, eDate, DataFormat)
        return json.loads(jsonData)

    def GetDailyData(self, StationID, SensorName, sDate, eDate, DataFormat):
        jsonData = self.client.service.GetDailyData(StationID, SensorName, sDate, eDate, DataFormat)
        return json.loads(jsonData)

    def GetCurrentDischarge(self, DataFormat):
        jsonData = self.client.service.GetCurrentDischarge(DataFormat)
        return json.loads(jsonData)

    def GetCurrentWaterLevels(self, DataFormat):
        jsonData = self.client.service.GetCurrentWaterLevels(DataFormat)
        return json.loads(jsonData)

    def GetCurrentPrecipTotals(self, DataFormat):
        jsonData = self.client.service.GetCurrentPrecipTotals(DataFormat)
        return json.loads(jsonData)

    def GetPrecipDistribution(self, StationID, DataFormat):
        jsonData = self.client.service.GetPrecipDistribution(StationID, DataFormat)
        return json.loads(jsonData)

    def GetPrecipStats(self, StationID, YearNumber, MonthNumber, DataFormat):
        jsonData = self.client.service.GetPrecipStats(StationID, YearNumber, MonthNumber, DataFormat)
        return json.loads(jsonData)
