import math
import operator

class AutocorrelationUtility:
	'''Transform the data fetched by Costeau into a dictionary
	that will be used to characterize the periodicity
	TODO:check the dest address'''
	
	def __init__(self,tracerouteIDsequence):
		self.tracerouteIDsequence=tracerouteIDsequence
		self.lagToScore=dict()


	def isAPeak(self,lag, listACFValues):
		if listACFValues[lag]> listACFValues[lag-1] and listACFValues[lag]> listACFValues[lag+1]:
		    if listACFValues[lag]> listACFValues[lag-2] and listACFValues[lag]> listACFValues[lag+2]:         
		        if listACFValues[lag]> listACFValues[lag-3] and listACFValues[lag]> listACFValues[lag+3]:
		            return True
		return False


	def computeACF(self):
		tracerouteIDsequence1=self.tracerouteIDsequence[:]
		tracerouteIDsequence2=self.tracerouteIDsequence[:]

		for k in range(0,len(self.tracerouteIDsequence)):
		    matchCount=0
		    for counter in range(0,len(tracerouteIDsequence2)):
		        if(tracerouteIDsequence1[counter]==tracerouteIDsequence2[counter]):
		            matchCount+=1

		    self.lagToScore[k]=matchCount
		    
		    tracerouteIDsequence1 = tracerouteIDsequence1[1:]
		    tracerouteIDsequence2 = tracerouteIDsequence2[:-1]
		return  self.lagToScore

	def getLag2ValuesOfPeaks(self):
		
		ACFValuesList=list()
		lagToValuesOfPeaks=dict()
		#print(self.lagToScore)
		for lag in self.lagToScore:
		    ACFValuesList.append(self.lagToScore[lag])

		for counter in range (3,len(ACFValuesList)-3):
		    if self.isAPeak(counter,ACFValuesList):
		        lagToValuesOfPeaks[counter]=ACFValuesList[counter]

		return lagToValuesOfPeaks


	def getPotentialPeriods(self,lagsOfPeaks,periodToCount):

		for counter in range(1,len(lagsOfPeaks)):
		    potentialPeriod= abs(int(lagsOfPeaks[counter])-int(lagsOfPeaks[counter-1]))

		    if potentialPeriod in periodToCount:
		        periodToCount[potentialPeriod]+=1

		    else:
		        periodToCount[potentialPeriod]=1

		return periodToCount

	def getPeriods(self,lagToPeakValues):
		candidatePeriodsToCount=dict()
		sorted_ByX=list()

		for peakLag in lagToPeakValues:
			sorted_ByX.append(peakLag)

		candidatePeriodsToCount=self.getPotentialPeriods(sorted_ByX, candidatePeriodsToCount)

		sorted_ByY=sorted(lagToPeakValues.items(),key=operator.itemgetter(1))
		sortedByYList=list()

		for c in sorted_ByY:
			sortedByYList.append(c[0])

		candidatePeriodsToCount=self.getPotentialPeriods(sortedByYList,candidatePeriodsToCount)
		
		return candidatePeriodsToCount