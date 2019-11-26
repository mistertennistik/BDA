import chart_studio.plotly  as py
import plotly.graph_objs as go
import plotly.offline as poff
from pandas import *


import math

class SunBurst(object):

	def __init__(self,bigMat,dicAssoc = None):

		self.df = bigMat.fillna(0)
		self.MIN = 0.0
		
		self.centerOfSun = ['ArrDelay_short','ArrDelay_long','ArrDelay_veryLong','ArrDelay_early','ArrDelay_onTime'] # ,'ArrDelay_veryLong','ArrDelay_early','ArrDelay_onTime'
		self.trace = None
		self.labels = []
		self.parents = []
		self.values = []
		self.ids = []

		self.layout = go.Layout(
    		margin = go.layout.Margin(t=0, l=0, r=0, b=0),
    		sunburstcolorway=["#636efa","#ef553b","#00cc96"]
			)

		self.addTotalToDf()

		#ajout du centre du sunburst
		self.prepareDatas()



		self.trace = go.Sunburst(
		 
		  labels= self.labels,
		  parents= self.parents,
		  values = self.values,
		  #branchvalues="total",
    	  outsidetextfont = {"size": 20, "color": "#377eb8"},
          marker = {"line": {"width": 2}},
		)

		self.fig = go.Figure([self.trace], self.layout)

		



	def addTotalToDf(self):
	    self.df['total'] = self.df.sum(axis=1)
	    print(self.df)

	def prepareDatas(self):
		print(self.df)
		# 1. initialisation du centre avec les ArrDelay_(short/onTime/long/veryLong/early)
			# "" dans parents et nom des vars dans labels

		totalOfSatArrDelay = 0
		for exp in self.centerOfSun :
			totalOfSatArrDelay+=self.df['total'][exp]
		

		self.labels.append('ArrDelay_')
		self.parents.append('')
		#self.values.append(totalOfSatArrDelay*100)
		for exp in self.centerOfSun :
			self.labels.append(exp)
			self.parents.append('ArrDelay_')
			self.values.append(self.df['total'][exp]/totalOfSatArrDelay*100) # quelle valeur ajouter ?  int(self.df['total'][exp]/totalOfSatArrDelay*100)
		

	
		for exp in self.centerOfSun :
			for A in enumerate(self.df[exp]):
				if A[1] > self.MIN and (self.df.columns[A[0]] not in self.centerOfSun): 
					self.labels.append(self.df.columns[A[0]]+'-'+exp)
					self.parents.append(exp)
					#print(self.df['total'][exp])
					self.values.append(A[1]/self.df['total'][exp]*100)
		
		

			

	def showSunBurst(self):

		poff.iplot(self.fig, filename='repeated_labels_sunburst')

