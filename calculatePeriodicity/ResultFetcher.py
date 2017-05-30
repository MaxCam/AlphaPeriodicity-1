from ripe.atlas.cousteau import AtlasResultsRequest


class ResultFetcherProxy:

	def __init__(self,msm_id,start,stop,probe_id):
		self.msm_id=msm_id
		self.start=start
		self.stop=stop
		self.probe_id=probe_id

	def fetchResults(self):

		kwargs = {
		    "msm_id": self.msm_id,
		    "start": self.start,
		    "stop": self.stop,
		    "probe_ids": self.probe_id
		}


		is_success, results = AtlasResultsRequest(**kwargs).create()
		return results


#trasforma in ResultFetcherProxy