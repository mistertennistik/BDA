#!/usr/bin/python
# -*- coding: utf-8 -*-


from vocabulary import Vocabulary
import sys,os

# class used to manage the file airPlane_2008.csv
#Year,Month,DayofMonth,DayOfWeek,DepTime,CRSDepTime,ArrTime,CRSArrTime,UniqueCarrier,FlightNum,TailNum,ActualElapsedTime,CRSElapsedTime,AirTime,ArrDelay,DepDelay,Origin,Dest,Distance,TaxiIn,TaxiOut,Cancelled,CancellationCode,Diverted,CarrierDelay,WeatherDelay,NASDelay,SecurityDelay,LateAircraftDelay
#2008,1,3,4,2003,1955,2211,2225,WN,335,N712SW,128,150,116,-14,8,IAD,TPA,810,4,8,0,,0,NA,NA,NA,NA,NA
class Flight(object):

	def __init__(self, l, voc):
		"""
		Instantiate a Flight from a line of the csv file
		"""
		self.vocabulary = voc
		d = l.split(",")
		self.fields = dict()
		try:
			self.fields['DayOfWeek'] =int(d[voc.mapping('DayOfWeek')])
		except:
			self.fields['DayOfWeek'] = None
		try:
			self.fields['DepTime'] =float(int(d[voc.mapping('DepTime')])/100)+ float(int(d[voc.mapping('DepTime')])%100)/100
		except:
			self.fields['DepTime'] = None
		try:
			self.fields['AirTime'] =int(d[voc.mapping('AirTime')])
		except:
			self.fields['AirTime'] = None
		try:
			self.fields['ArrDelay'] =int(d[voc.mapping('ArrDelay')])
		except:
			self.fields['ArrDelay'] = None
		try:
			self.fields['DepDelay'] =int(d[voc.mapping('DepDelay')])
		except:
			self.fields['DepDelay'] = None
		try:
			self.fields['ArrTime'] =int(d[voc.mapping('ArrTime')])
		except:
			self.fields['ArrTime'] = None
		try:
			self.fields['Distance'] =int(d[voc.mapping('Distance')])
		except:
			self.fields['Distance'] = None
		try:
			self.fields['Month'] =d[voc.mapping('Month')]
		except:
			self.fields['Month'] = None
		try:
			self.fields['DayOfMonth'] =int(d[voc.mapping('DayOfMonth')])
		except:
			self.fields['DayOfMonth'] = None
		try:
			self.fields['TaxiIn'] =int(d[voc.mapping('TaxiIn')])
		except:
			self.fields['TaxiIn'] = None
		try:
			self.fields['TaxiOut'] =int(d[voc.mapping('TaxiOut')])
		except:
			self.fields['TaxiOut'] = None
		try:
			self.fields['CarrierDelay'] =int(d[voc.mapping('CarrierDelay')])
		except:
			self.fields['CarrierDelay'] = 0
		try:
			self.fields['WeatherDelay'] =int(d[voc.mapping('WeatherDelay')])
		except:
			self.fields['WeatherDelay'] = 0
		try:
			self.fields['SecurityDelay'] =int(d[voc.mapping('SecurityDelay')])
		except:
			self.fields['SecurityDelay'] = 0
		try:
			self.fields['LateAircraftDelay'] =int(d[voc.mapping('LateAircraftDelay')])
		except:
			self.fields['LateAircraftDelay'] = 0
		try:
			self.fields['Origin'] =d[voc.mapping('Origin')]
		except:
			self.fields['Origin'] = None
		try:
			self.fields['Dest'] =d[voc.mapping('Dest')]
		except:
			self.fields['Dest'] = None

	def __str__(self):
		return "TEEEST"

	def getValue(self,field):
		ret = None
		if field in self.fields:
			ret = self.fields[field]
		return ret

	def rewrite(self):
		""" Rewrite the flight according to the vocabulary voc (voc is a Vocabulary)"""
		rw=[]
		for part in self.vocabulary.getPartitions():
			for partelt in part.getModalities():
				val=self.getValue(part.getAttName())
				mu = partelt.getMu(val)
				rw.append(mu)
		return rw


	def rewriteWithLabel(self):
		value  = self.rewrite();
		labels = ['DayOfWeek_beginning','DayOfWeek_end','DayOfWeek_weekend','DepTime_morning','DepTime_midday','DepTime_afternoon','DepTime_evening','DepTime_night','ArrTime_morning','ArrTime_midday','ArrTime_afternoon','ArrTime_evening','ArrTime_night','AirTime_veryShort','AirTime_short','AirTime_medium','AirTime_long','AirTime_veryLong','ArrDelay_early','ArrDelay_onTime','ArrDelay_short','ArrDelay_acceptable','ArrDelay_long','ArrDelay_veryLong','DepDelay_none','DepDelay_short','DepDelay_acceptable','DepDelay_long','DepDelay_veryLong','Distance_veryShort','Distance_short','Distance_medium','Distance_long','Distance_veryLong','Month_winter','Month_spring','Month_summer','Month_autumn','DayOfMonth_beginning','DayOfMonth_middle','DayOfMonth_end','TaxiIn_short','TaxiIn_medium','TaxiIn_long','TaxiOut_short','TaxiOut_medium','TaxiOut_long','CarrierDelay_none','CarrierDelay_short','CarrierDelay_acceptable','CarrierDelay_long','CarrierDelay_veryLong','WeatherDelay_none','WeatherDelay_short','WeatherDelay_acceptable','WeatherDelay_long','WeatherDelay_veryLong','SecurityDelay_none','SecurityDelay_short','SecurityDelay_acceptable','SecurityDelay_long','SecurityDelay_veryLong','LateAirCraftDelay_none','LateAirCraftDelay_short','LateAirCraftDelay_acceptable','LateAirCraftDelay_long','LateAirCraftDelay_veryLong','Origin_main','Origin_big','Origin_medium','Origin_small','Dest_main','Dest_big','Dest_medium','Dest_small']
		return dict(zip(labels,value))

if __name__ == "__main__":
	if len(sys.argv)  < 2:
		print("Usage: python flight.py <vocfile.csv>")
	else:
		if os.path.isfile(sys.argv[1]): 
			voc = Vocabulary(sys.argv[1])
			line= "2008,1,3,4,1103,1955,2211,2225,WN,335,N712SW,128,150,116,-14,8,IAD,TPA,810,4,8,0,,0,NA,NA,NA,NA,NA"
			f = Flight(line,voc)
			print(f.rewrite())

