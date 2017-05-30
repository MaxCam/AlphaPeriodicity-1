class ResultDataAdapter:
	'''Transform the data fetched by Costeau into a dictionary
	that will be used to characterize the periodicity'''

	def addNewTracerouteEntry(self,sourceDestionationID,idProbeAnchorToIdsM,prbIdSource,idMeas,reachingTarget,destinationAddress,ipNumberProtocol,timeStampOfNew,traceroute,parisId):
		idProbeAnchorToIdsM[sourceDestionationID] = dict()
		idProbeAnchorToIdsM[sourceDestionationID][0] = dict()
		idProbeAnchorToIdsM[sourceDestionationID][0]["probeId"]=str(prbIdSource)
		idProbeAnchorToIdsM[sourceDestionationID][0]["idMeas"] = str(idMeas)
		idProbeAnchorToIdsM[sourceDestionationID][0]["reachingTarget"] = str(reachingTarget)
		idProbeAnchorToIdsM[sourceDestionationID][0]["destinationAddress"] = str(destinationAddress)
		idProbeAnchorToIdsM[sourceDestionationID][0]["ipNumberProtocol"] = str(ipNumberProtocol)
		idProbeAnchorToIdsM[sourceDestionationID][0]["timeStampOfNew"] = str(timeStampOfNew)
		idProbeAnchorToIdsM[sourceDestionationID][0]["traceroute"] = str(traceroute)
		idProbeAnchorToIdsM[sourceDestionationID][0]["paris_ids"] = dict()

		for counter in range(0, 16):
		    idProbeAnchorToIdsM[sourceDestionationID][0]["paris_ids"][counter] = 0 

		idProbeAnchorToIdsM[sourceDestionationID][0]["paris_ids"][parisId] = 1

	def updateRecord(self,sourceDestionationID,idProbeAnchorToIdsM,prbIdSource,idMeas,reachingTarget,destinationAddress,ipNumberProtocol,timeStampOfNew,traceroute,parisId):
			   
		matched = idProbeAnchorToIdsM[sourceDestionationID]
		presenti = len(matched)
		TracealreadyPresent = False

		for rec in matched:

		    if (str(idProbeAnchorToIdsM[sourceDestionationID][rec]["traceroute"]).strip() == str(traceroute).strip()):
		        TracealreadyPresent = True
		        k = str(idProbeAnchorToIdsM[sourceDestionationID][rec]["timeStampOfNew"]) + str(timeStampOfNew)
		        break

		if (TracealreadyPresent is True):
		    idProbeAnchorToIdsM[sourceDestionationID][rec]["timeStampOfNew"] = str(k)
		    idProbeAnchorToIdsM[sourceDestionationID][rec]["paris_ids"][parisId] += 1

		if (TracealreadyPresent is False):
		    idProbeAnchorToIdsM[sourceDestionationID][presenti] = dict()
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["probeId"] = str(prbIdSource)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["idMeas"] = str(idMeas)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["reachingTarget"] = str(reachingTarget)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["destinationAddress"] = str(destinationAddress)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["ipNumberProtocol"] = str(ipNumberProtocol)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["timeStampOfNew"] = str(timeStampOfNew)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["traceroute"] = str(traceroute)
		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["paris_ids"] = dict()
		    
		    for counter in range(0, 16):
		        idProbeAnchorToIdsM[sourceDestionationID][presenti]["paris_ids"][counter] = 0

		    idProbeAnchorToIdsM[sourceDestionationID][presenti]["paris_ids"][parisId] = 1


	def extractMetadataRecord(self,data, recordCounter):
			ipNumberProtocol = data[recordCounter]["af"]
			prbIdSource = data[recordCounter]["prb_id"]
			destinationAddress = data[recordCounter]["dst_addr"]
			idMeas = data[recordCounter]["msm_id"]
			parisId = int(data[recordCounter]["paris_id"])
			timeStampOfNew = str(data[recordCounter]["timestamp"]) + ";;"
			return ipNumberProtocol,prbIdSource,destinationAddress,idMeas,parisId,timeStampOfNew

	def buildTraceroute(self,recordCounter,data):
		traceroute=""
		for hopCounter in range(0, len(data[recordCounter]["result"])):
			try:
			    currentIp = data[recordCounter]["result"][hopCounter]["result"][0]["from"]
			    traceroute = traceroute + currentIp + ";;"
			except:
			    traceroute = traceroute + "*" + ";;"
		return traceroute

	def __init__(self,results):
		self.results=results

	def adaptResults(self):
		data=self.results

		idProbeAnchorToIdsM=dict()
		traceroute=""

		for recordCounter in range(0, len(data)):
			ipNumberProtocol,prbIdSource,destinationAddress,idMeas,parisId,timeStampOfNew=self.extractMetadataRecord(data,recordCounter)
			sourceDestionationID = str(prbIdSource) + "-" + str(destinationAddress)
			
			reachingTarget = True #TODO fare verifica su controllo del target
			sourceAddress = data[recordCounter]["src_addr"]

			traceroute= self.buildTraceroute(recordCounter,data)

			if (sourceDestionationID not in idProbeAnchorToIdsM.keys()):
				self.addNewTracerouteEntry(sourceDestionationID,idProbeAnchorToIdsM,prbIdSource,idMeas,reachingTarget,destinationAddress,ipNumberProtocol,timeStampOfNew,traceroute,parisId)
			else:
				self.updateRecord(sourceDestionationID,idProbeAnchorToIdsM,prbIdSource,idMeas,reachingTarget,destinationAddress,ipNumberProtocol,timeStampOfNew,traceroute,parisId)
			    

			traceroute = ""

		return idProbeAnchorToIdsM