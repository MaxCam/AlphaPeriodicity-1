import datetime
class PeriodicityCharacterizer:
	'''Transform the data fetched by Costeau into a dictionary
	that will be used to characterize the periodicity
	TODO:check the dest address'''
	
	def __init__(self,candidatePeriodsToCount,tracerouteIDsequence):
		self.candidatePeriodsToCount=candidatePeriodsToCount
		self.tracerouteIDsequence=tracerouteIDsequence
		self.periodicityFound=False

	def differentTraceroute(self,gram):
		tracerouteID=set()
		for id in gram:
			tracerouteID.add(id)

		return len(tracerouteID)


	def computeTollerance(self,lengthGram):
		return 0


	def hamdist(self,seq1, seq2):
		diffs = abs(len(seq1)-len(seq2))
		for ch1, ch2 in zip(seq1, seq2):
		    if ch1 != ch2:
		        diffs += 1
		return diffs

	def cyclic_equiv(self,u, v):
		n, i, j = len(u), 0, 0
		if n != len(v):
			return False
		while i < n and j < n:
			k = 1
			while k <= n and u[(i + k) % n] == v[(j + k) % n]:
				k += 1
			if k > n:
				return True
			if u[(i + k) % n] > v[(j + k) % n]:
				i += k
			else:
				j += k
		return False

	def insertNewPattern(self,patternList,gram):
		newPattern=""

		for tracerouteId in gram:
			newPattern+=str(tracerouteId)+"-"

		newPattern=newPattern[:-1]

		for tracerouteID in patternList:
			if(self.cyclic_equiv(tracerouteID,newPattern)):
				return False
			if(newPattern in tracerouteID):
				return False

		if(self.differentTraceroute(gram)==1):
			return False
			
		patternList.add(newPattern)
		return True

		return pattern

	def getPatterns(self):
		patternList=set()

		for periodicityLength in self.candidatePeriodsToCount.keys():
			periodLentgth = int(periodicityLength)
			ngramsSplitted =[self.tracerouteIDsequence[i:i+periodLentgth] for i in range(0, len(self.tracerouteIDsequence), periodLentgth)]
			prevGram=ngramsSplitted[0]
			count=0
			for gram in ngramsSplitted:
				if(count==0):
					count+=1
				else:
					if self.hamdist(gram,prevGram)<=self.computeTollerance(len(gram)):
						self.insertNewPattern(patternList,gram)

					prevGram=gram
		return patternList

	def getPeriodicities(self,patterns,tracerouteIDsequence,startTime):
		#qui c'e qualche bug!
		periodicityToStartAndStop=dict()
		periodicitaIncorso=False
		for pattern in patterns:

			patternSplitted=pattern.split("-")
			patternInList=list()

			for counter in range(0,len(patternSplitted)):
				patternInList.append(int(patternSplitted[counter]))

			periodLentgth = len(patternInList)
			ngramsSplitted =[self.tracerouteIDsequence[i:i+periodLentgth] for i in range(0, len(self.tracerouteIDsequence), periodLentgth)]
			prevGram=patternInList

			lag=periodLentgth
			periodicitaIncorso=False
			for gram in ngramsSplitted:

				#attenzione:deve essere lunga almeno 2!
				if self.hamdist(gram,patternInList)<=self.computeTollerance(len(gram)):
					if(periodicitaIncorso==False):
						periodicitaIncorso=True
						start=lag-periodLentgth
				else:
					if(periodicitaIncorso==True):
						periodicitaIncorso=False
						if(lag-start>periodLentgth):
							periodicityToStartAndStop[str(patternInList)+"-"+str(start)]=[self.getDate(startTime+(start*15*60)),self.getDate(startTime+(lag*15*60))]
				lag+=1*periodLentgth
			#	prevGram=gram
		if(periodicitaIncorso==True):
			periodicitaIncorso=False
			periodicityToStartAndStop[str(patternInList)+"-"+str(start)]=[self.getDate(startTime+(start*15*60)),self.getDate(startTime+(lag*15*60))]
		return periodicityToStartAndStop

	def removeDuplicate(self,patterns):
		patternsFiltered=set()
		for pattern in patterns:
			i=(pattern+pattern).find(pattern,1,-1)
			if(i==-1):
				patternsFiltered.add(pattern)
			else:
				patternsFiltered.add(pattern[:i])
		return patternsFiltered

	def getDate(self,unixTimestamp):
		#return unixTimestamp
		return datetime.datetime.fromtimestamp(int(unixTimestamp)).strftime('%Y-%m-%d %H:%M:%S')
