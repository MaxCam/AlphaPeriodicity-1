import datetime

class ResultDataAdapter:
	'''Transform the data fetched by Costeau into a dictionary
	that will be used to characterize the periodicity
	TODO:check the dest address'''
	
	def __init__(self,start,results):
		self.results=results
		self.start=start

	def extractMetadataRecord(self,data, recordCounter):
			ipNumberProtocol = data[recordCounter]["af"]
			prbIdSource = data[recordCounter]["prb_id"]
			destinationAddress = data[recordCounter]["dst_addr"]
			idMeas = data[recordCounter]["msm_id"]
			parisId = int(data[recordCounter]["paris_id"])
			timestamp = str(data[recordCounter]["timestamp"])
			return ipNumberProtocol,prbIdSource,destinationAddress,idMeas,parisId,timestamp

	def buildTraceroute(self,recordCounter,data):
		traceroute=""
		for hopCounter in range(0, len(data[recordCounter]["result"])):
			try:
			    currentIp = data[recordCounter]["result"][hopCounter]["result"][0]["from"]
			    traceroute = traceroute + currentIp + ";;"
			except:
			    traceroute = traceroute + "*" + ";;"
		return traceroute.strip()

	def adaptResults(self):
		data=self.results
		prevTime=self.start

		tracerouteIDSequence=list()
		tracerouteToId=dict()

		tracerouteIdCounter=100

		for recordCounter in range(0, len(data)):
			ipNumberProtocol,prbIdSource,destinationAddress,idMeas,parisId,timestamp=self.extractMetadataRecord(data,recordCounter)
			traceroute= self.buildTraceroute(recordCounter,data)

			if(traceroute not in tracerouteToId.keys()):
				tracerouteToId[traceroute]=tracerouteIdCounter
				tracerouteIdCounter+=100

			'''missing traceroute, e.g. probe disconnected'''
			while(int(prevTime)<int(timestamp)-920):
				prevTime=int(prevTime)+900
				tracerouteIDSequence.append(0)

			tracerouteIDSequence.append(int(tracerouteToId[traceroute]))
			prevTime=timestamp

			traceroute = ""

		return tracerouteToId,tracerouteIDSequence

	def getGDBdiagram(self,tracerouteSequence):
		startTime=self.start
		counter=0
		gdbdstring=""

		prev=0

		gdbdstring+=("date,a\n")

		for tracerouteID in tracerouteSequence:
			gdbdstring+=(str(self.getDate((60*15*counter)+startTime))+","+str(prev)+"\n")
			gdbdstring+=(str(self.getDate((60*15*counter)+startTime))+","+str(tracerouteID)+"\n")
			prev=tracerouteID
			counter+=1
#self.getDate((60*15*counter)+startTime))
		return gdbdstring

	def getDate(self,unixTimestamp):
		#return unixTimestamp
		return datetime.datetime.fromtimestamp(int(unixTimestamp)).strftime('%d/%m/%Y %H:%M:%S')
