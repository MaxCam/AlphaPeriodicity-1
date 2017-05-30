from ResultFetcher import ResultFetcherProxy
from DataAdapter import ResultDataAdapter
from AutocorrelationUtility import AutocorrelationUtility
from PeriodicityCharacterizer import PeriodicityCharacterizer

class Main:
	def __init__(self,probe,defaultStart,defaultEnd,defaultMeasurement):
		self.probe=probe
		self.defaultStart=defaultStart
		self.defaultEnd=defaultEnd
		self.defaultMeasurement=defaultMeasurement

	def getPeriodicities(self):
		resultFetcher=ResultFetcherProxy(self.defaultMeasurement,self.defaultStart,self.defaultEnd,self.probe)
		data=resultFetcher.fetchResults()
		#print(data)
		dataAdapter=ResultDataAdapter(self.defaultStart,data)
		tracerouteToID,tracerouteIDsequence=dataAdapter.adaptResults()

		# print(tracerouteToID)

		gdbd=dataAdapter.getGDBdiagram(tracerouteIDsequence)

		#out_file = open("gdbData.tsv","w")
		#out_file.write(gdbd)
		#out_file.close()

		autocorrelationUtility=AutocorrelationUtility(tracerouteIDsequence)
		lagToACFValue=autocorrelationUtility.computeACF() #dictionaru
		lagToPeakValues=autocorrelationUtility.getLag2ValuesOfPeaks()
		candidatePeriodsToCount=autocorrelationUtility.getPeriods(lagToPeakValues)

		periodicityCharacterizer=PeriodicityCharacterizer(candidatePeriodsToCount,tracerouteIDsequence)
		patterns=periodicityCharacterizer.getPatterns()
		patterns=periodicityCharacterizer.removeDuplicate(patterns)


		periodicityToStartAndStop=periodicityCharacterizer.getPeriodicities(patterns,tracerouteIDsequence,self.defaultStart)

		# print(tracerouteIDsequence)
		# print(lagToACFValue)
		#print(lagToPeakValues)
		#print(candidatePeriodsToCount)

		#print(periodicityToStartAndStop)

		response_json = {}


		children = []
		for item in periodicityToStartAndStop:
		    children.append({"periodic pattern" : item[:-3],
		                     "end" : periodicityToStartAndStop[item][1],
		                     "start" : periodicityToStartAndStop[item][0]})

		response_json["Detected Periodicities"] = children



		children = []
		for item in tracerouteToID:
		    children.append({"id" : str(tracerouteToID[item]),
		                     "traceroute" : item})

		response_json["tracerouteToId"] = children
		response_json["message"] = 'Periodicity Report. The list of periodicities follows. The \'periodic pattern\' field shows the periodic pattern of a spotted periodicity. Each path involved in the \
pattern is represented with a path id. Fields \'start\' and \'end\' show the periodic interval. The \'traceroute\' fields contain the paths observed in the time interval specified in the query. The \'id\' \
at the end of thepath is the path id. '
		#response_json["probe"]=self.probe
		#response_json["start"]=self.defaultStart
		#response_json["end"]=self.defaultEnd
		#response_json["measurement"]=self.defaultMeasurement
		#print(gdbd)
		return response_json	