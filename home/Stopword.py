from BinarySearch import *
import os
stop_words = [line.strip() for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"stop_words.txt"), 'r')]

def IsStopWord(word):
	if binarySearch(stop_words, word) != -1:
		return True
	else:
		return False
