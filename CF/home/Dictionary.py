from WordFrequency import *
from BinarySearch import *
import os

class Dictionary:
	def __init__(self):
		self.words = [] # List of words and frequency

	def indexOf(self, word):
		for i in range(len(self.words)):
			if self.words[i].word == word:
				return i
		return -1

	def indexOfS(self, word):
		first = 0
		last = len(self.words) - 1
		found = -1

		while first <= last and found == -1:
			midpoint = (first + last) // 2
			if self.words[midpoint].word == word:
				found = midpoint
			else:
				if word < self.words[midpoint].word:
					last = midpoint - 1
				else:
					first = midpoint + 1

		return found

	def addWord(self, word):
		if self.indexOf(word) == -1:		# Word not yet in Dictionary
			self.words.append(WordFrequency(word))
		else:
			self.words[self.indexOf(word)].AddCount()

	def addWords(self, words):
		for word in words:
			self.addWord(word)

	def loadDictionary(self):
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Output-stemmed.txt"), "r") as text_file:
			for line in text_file:
				line = line[:-1]
				line_split = line.split(' ')
				self.words.append(WordFrequency(line_split[0],int(line_split[1])))

	def minimumFreq(self, count):
		for i in reversed(range(len(self.words))):
			if self.words[i].count <= 3:
				del self.words[i]
