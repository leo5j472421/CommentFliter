class WordFrequency:
	def __init__(self, word, count=1):
		self.word = word
		self.count = count

	def AddCount(self):
		self.count += 1

	def __cmp__(self, other):
		return cmp(self.word, other.word)
