import pandas as pd

class Extraction(object):

	def __init__(self,vector):
		#self.voc = voc # may be useless
		self.vect = vector # pd dataFrame
		self.border = 0.6 # constant to keep only assoc > constant in sumUpAssoc
		
		self.entitled = vector.columns
		self.sumUpAssoc = {k: [] for k in vector.columns} # sum up of each prop with others prop associated

		self.bigMat = pd.DataFrame(index = self.entitled, columns=self.entitled)


	def tuppletsWhichRespectNConditions(self, listConds):
		dfTemp = self.vect.copy() #peut etre deep copy
		for cond in listConds:
			dfTemp = getLinesFromVectAndCond(dfTemp,cond)

		return dfTemp

	def getLinesFromVectAndCond(self,vect,cond):
		return vect.query(cond)


	def getLinesWhichRespect(self,cond):
		return self.vect.query(cond)

	def sumUp(self,vector):
		'''
			return the sum of each column for the vector(dataframe)
		'''
		return vector.sum(axis = 0, skipna = False)/len(vector)

	def bigMatConstructor(self):
		#print("ICI")
		#print(self.bigMat)
		#print(self.entitled)
		ll = []
		request = ""

		for e in self.entitled:
			#ind = e.find(',')
			#e = e[:ind] + "" + e[ind:]
			request += e+ " > 0"
			ll.append(self.sumUp(self.getLinesWhichRespect(request)))
			request=""
		self.bigMat = pd.DataFrame(data= ll,index = self.entitled, columns=self.entitled)
		print(self.bigMat)
		
	def assoc(self,v, vp):
		dep = self.dep(v,vp)
		if dep<=1:
			return 0
		else:
			return 1 - (1/dep)

	def dep(self,cond,vp):
		return cover(vp,self.subset(cond))/cover(vp,self.vect)

	"""def cover(self,vect):"""




	# voir comment appliquer la condition au dataframe
	# v est une simple propriété ou une vraie condition ? 	
	def subset(self,cond):
		return self.vect[cond]

	"""def runExtraction(self):
		'''
			create the dict with each property and its significant 
			correlated properties (with assoc >= self.border)
		'''
		for i in range(len(self.entitled)-1):
			for j in range(i+1,len(self.entitled)-1)
			a = assoc(self.entitled[i], self.entitled[j])
			if a >= self.border:
				self.sumUpAssoc[self.entitled[i]].append(self.entitled[i+1])"""

"""if __name__ == "__main__":"""
 	
