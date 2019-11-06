#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
from vocabulary import *
from flight import Flight

from operator import add
import pandas as pd


import matplotlib.pyplot as plt
from wordcloud import WordCloud



from extraction import Extraction

class RewriterFromCSV(object):

	def __init__(self, voc, df):
		"""
		Translate a dataFile using a given vocabulary
		"""
		self.vocabulary = voc
		self.dataFile = df
		self.sumUp = [0 for i in range(67)]
		self.dataFrameTemp = []
		self.dataFrame = None


		print


	def readAndRewrite(self):
		self.dataFrame = None
		self.sumUp = [0 for i in range(67)]
		self.dataFrameTemp = []
		try:
			with open(self.dataFile, 'r') as source:
				for line in source:
					line = line.strip()
					if line != "" and line[0] != "#":
		
						f = Flight(line,self.vocabulary)
						##Do what you need with the rewriting vector here ...
						self.dataFrameTemp.append(f.rewriteWithLabel())
				

						self.sumUp = list(map(add, self.sumUp, f.rewrite()))
				self.dataFrame = pd.DataFrame(self.dataFrameTemp)
				#print(self.dataFrame.head(10))
				#print(self.sumUp)
				#print(self.dataFrame.sum(axis = 0, skipna = False).sort_values())


		except:
			raise Exception("Error while loading the dataFile %s"%(self.dataFile))

	def sumUpToDict(self):
		self.readAndRewrite()
		return (self.dataFrame.sum(axis = 0, skipna = False)/len(self.dataFrame)).to_dict()

	def wordCloudGenerator(self):
		d = self.sumUpToDict()
		wordcloud = WordCloud(max_font_size=350, max_words=30, background_color="black",width=1600, height=800)
		wordcloud.generate_from_frequencies(frequencies=d)
		plt.figure(figsize=(20,10), facecolor='k')
		plt.imshow(wordcloud, interpolation="bilinear")
		print(self.dataFrame)
		print(self.sumUpToDict())
		plt.axis("off")
		plt.show()



if __name__ == "__main__":
 	if len(sys.argv)  < 3:
 		print("Usage: python flight.py <vocfile> <dataFile>")
 	else:
 		if os.path.isfile(sys.argv[1]): 
 			voc = Vocabulary(sys.argv[1])
	 		if os.path.isfile(sys.argv[2]): 
	 			rw = RewriterFromCSV(voc, sys.argv[2])
	 			#rw.readAndRewrite()
	 			#rw.wordCloudGenerator()
	 			#print(rw.dataFrame)
	 			print(rw.sumUpToDict())
	 			ex = Extraction(rw.dataFrame)
	 			ex.bigMatConstructor()


	 		else:
	 			print("Data file %s not found"%(sys.argv[2]))
	 	else:
	 		print("Voc file %s not found"%(sys.argv[2]))
