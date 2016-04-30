import sys
import config
import apis
import re
import distance

class searchAll:
	
	wordsToSkip = ['the','of','and']

	def __init__(self, api):
		# load api config
		try:
			if api in config.APIS:
				apiClass = getattr(apis, api)
				self.api = apiClass(config.APIS[api])
				self.tags = {}
			else:
				raise Exception("Given API does not exist")
		except Exception as e:
			print("Load error: " + str(e))
			exit()

	def tagReduce(self, word):
		# simplify words to use as tags
		reg = re.compile("[a-z]*")
		tag = reg.match(word.lower()).group()
		if tag or tag is not None or tag not in self.wordsToSkip:
			return tag

	def similarity(self, word1, word2):
		# Score function may vary and for sure can be improved
		# I used distance module here
		ldist = distance.levenshtein(word1, word2)
		hdist = 0 #distance.hamming(word1, word2) requires equal length e.g. padding
		score = ldist * 1# + hdist * 0
		return score

	def itemHandler(self, item):
		# process item here
		tags = map(self.tagReduce, item['name'].split()) # [optional] include description
		for tag in tags:
			if tag not in self.tags:
				# initiate set for the tag
				self.tags[tag] = set()
			self.tags[tag].add(item['name'])

		#print(item['name'])
		#print(item['id'])
		self.itemCount += 1
		pass

	def findKey(self, keyword, output=True):
		if keyword in self.tags:
			if output:
				print(self.tags[keyword])
			else:
				return self.tags[keyword]
		else:
			minScore = 100
			bestTag = ''
			for tag in self.tags:
				score = self.similarity(keyword, tag)
				#print(score, tag, keyword)
				if score < minScore:
					minScore = score
					bestTag = tag
			#print("MAX SCORE : {0}".format(minScore))
			#print("BEST TAG : {0}".format(bestTag))
			if output:
				print("Did you mean {0}?".format(bestTag))
			else:
				return self.tags[bestTag]

	def search(self, keyword):
		keywords = keyword.split()
		groups = []
		# multiple keywords
		if len(keywords) > 1:
			for key in keywords:
				groups.append(self.findKey(key, output=False))
			print(set.intersection(*groups))
		# single keyword
		else:
			self.findKey(keyword)

	def indexAll(self):

		self.itemCount = 0
		self.api.fetchAll(self.itemHandler)
		print("TOTAL ITEMS : {0}".format(self.itemCount))
		#print("TAGS : " + str(self.tags))


if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print("Please provide an API to fetch from")
		print("Usage: python3 searchAll.py {apiName}")
		exit()

	app = searchAll(sys.argv[1])
	app.indexAll()

	keyword = True
	while not keyword or keyword not in ['exit','quit','q']:
		keyword = input("Search: ")
		app.search(keyword)

	print("SearchAll ended. Goodbye")