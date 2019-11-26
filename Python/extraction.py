import pandas as pd

class Extraction(object):

	def __init__(self,vector):
		#self.voc = voc # may be useless
		self.vect = vector # pd dataFrame
		self.border = 0.6 # constant to keep only assoc > constant in sumUpAssoc
		
		self.entitled = vector.columns
		self.sumUpAssoc = {k: dict() for k in vector.columns} # sum up of each prop with others prop associated

		self.bigMat = pd.DataFrame(index = self.entitled, columns=self.entitled)

		self.matFromDict = None

	#OK
	def tuppletsWhichRespectNConditions(self, listConds):
		dfTemp = self.vect.copy() #peut etre deep copy
		for cond in listConds:
			dfTemp = self.getLinesFromVectAndCond(dfTemp,cond)

		return dfTemp

	#OK	
	def getLinesFromVectAndCond(self,vect,cond):
		return vect.query(cond)


	def getLinesWhichRespect(self,cond):
		return self.vect.query(cond)

	def sumUp(self,vector):
		'''
			return the sum of each  for the vector(dataframe)
		'''
		return vector.sum(axis = 0, skipna = False)/len(vector)
	def sumUp2(self,vector):
		return 	vector.sum(axis = 0, skipna = False)/len(self.vect)

		
	def assoc(self,v, vp):
		dep = self.dep(v,vp)
		if dep<=1:
			return 0
		else:
			return 1 - (1/dep)

	def dep(self,v,vp):
		return self.cover(vp,self.subset(v))/self.cover(vp,self.vect)

	def cover(self,vp,set):
		#print(self.sumUp(set[vp]))
		return self.sumUp(set[vp])

	
	def subset(self,v):
		return self.getLinesFromVectAndCond(self.vect,v+">0")
	
	def dicAssocConstructor(self):
		for i in self.entitled:
			for j in self.entitled:
				if i!=j:
					#print(val,j)
					a = self.assoc(i,j)
					#if a>0:
					self.sumUpAssoc[i][j] = a

	def matFromDictConstructor(self):
		self.dicAssocConstructor()
		self.matFromDict = pd.DataFrame(self.sumUpAssoc)
		return self.matFromDict.fillna(0)

	def bigMatConstructor(self):
		"""
				Construit une matrice qui associe à quel point [0,1] un mot du vocabulaire
				est lié à un autre.
		"""
		ll = []
		request = ""

		for e in self.entitled:
			#ind = e.find(',')
			#e = e[:ind] + "" + e[ind:]
			request += e+ " > 0"
			ll.append(self.sumUp2(self.getLinesWhichRespect(request)))
			request=""
		self.bigMat = pd.DataFrame(data= ll,index = self.entitled, columns=self.entitled).fillna(0)
		print(self.bigMat)

"""if __name__ == "__main__":"""
 	
