from BinarySearch import *
import os
valid_domain = [line.strip() for line in open( os.path.join(os.path.dirname(os.path.abspath(__file__)),'tlds-alpha-by-domain.txt'), 'r')]

def IsValidUrl(word):
	if binarySearch(valid_domain, word.split(".")[-1].upper()) != -1:
		return True
	else:
		return False
