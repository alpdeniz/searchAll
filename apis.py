import requests

class BaseAPI:
	def __init__(self, config):
		self.config = config
		self.currentOffset = 0
		print("{0} loaded".format(self.config['apiName'])) #, str(self.config)))

	def buildURL(self):
		return self.config['apiUrl'] + ("&{0}={1}&{2}={3}".format(self.config['offsetParam'], self.currentOffset, self.config['batchParam'], self.config['batchSize']))

	def fetchAll(self, handler):
		print("fetching data")
		# reset offset
		self.currentOffset = 0
		self.loading = True
		# get all games
		while self.loading:
			self.fetch(handler)

		print("Fetch complete")

class GiantBomb(BaseAPI):

	def fetch(self, handler):
		url = self.buildURL()
		data = requests.get(url, headers={'User-Agent': 'SearchAll Engine v0.01'}).json()['results']
		batch = len(data)
		print("Got {0} games".format(batch))
		self.currentOffset += batch
		for d in data:
			handler(d)
		
		if batch < self.config['batchSize'] or self.currentOffset >= self.config['maxItems']:
			self.loading = False


class OtherApi(BaseAPI):

	def fetch(self, handler):
		pass