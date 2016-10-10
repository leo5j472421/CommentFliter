import re
from urllib.parse import urlparse
from Url import *
from Stopword import *
from stemming.porter2 import stem
from Dictionary import *

class Comment:
	def __init__(self, content=""):
		self.flag = ""
		self.content = content
		self.bagofwords = []

	def tokenize(self):
		temp = str(self.content)
		out = ""
		skip = False
		site_count = 0
		# 1. All are lower
		temp = temp.lower()
		# 2. Remove @userxxx if possible
		temp = temp.split(' ')
		# 3. 
		reg_url = re.compile(r'^(?:(?:https?|ftp):\/\/)?(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$', re.IGNORECASE)
		reg_pro = re.compile(r"~^(?:f|ht)tps?://~i")
		reg_url = re.compile(r'^(?:(?:https?|ftp):\/\/)?(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$', re.IGNORECASE)
		reg_ip = re.compile(r'(?:(?:https?|ftp):\/\/)?(?:[0-9]{1,3}\.){3}[0-9]{1,3}', re.IGNORECASE)
		reg_pro = re.compile(r"~^(?:f|ht)tps?://~i")
		for c in reversed(list(range(len(temp)))):
			try:	
				if temp[c][0] == '@':
					del temp[c]
					continue
			except IndexError:
				continue
			if '.' in temp[c]:
				if reg_url.match(temp[c]) is not None:
					if reg_ip.match(temp[c]) is not None:
						if reg_pro.match(temp[c]) is None:
							temp[c] = "http://" + temp[c]
						out += "#" + urlparse(temp[c]).netloc + " "
						del temp[c]
					elif IsValidUrl(temp[c]):
						if reg_pro.match(temp[c]) is None:
							temp[c] = "http://" + temp[c]
						out += "#" + urlparse(temp[c]).netloc + " "
						del temp[c]
		temp = " ".join(temp)
		last_letter = ''
		consecutive_letter_count = 1
		for c in reversed(list(range(len(temp)))):# Start reading from end
			if not skip:					# Skip iteration
				if temp[c].isalpha():		# 2. Accept all alphabet
					if last_letter == temp[c]:
						consecutive_letter_count += 1
						if consecutive_letter_count <= 3:
							out = temp[c] + out
					else:
						consecutive_letter_count = 1
						last_letter = temp[c]
						out = temp[c] + out
				elif temp[c:c+1] == "\\n":	# 3. Read \n as whitespace
					out = " " + out
					skip = True
				elif temp[c] == "'":		# 4. Delete ' (don't -> dont)
					out = "" + out
				elif temp[c] == " ":
					out = " " + out
				else:						# 5. Else, " "
					out = " " + out
			else:
				skip = False
		out = out.split(' ')
		out = [ x for x in out if len(x) > 2 ] # 6. Accept words with more then 2 letters only
		#stop word
		out = [x for x in out if not IsStopWord(x)]
		#Stem
		for i in range(len(out)):
			if out[i][0] != '#':
				out[i] = stem(out[i])
		return out

	def BagOfWords(self, dictionary):
		raw = self.tokenize()
		bow = Dictionary()
		out = self.flag + " "
		for ctr in reversed(list(range(len(raw)))):
			i = dictionary.indexOfS(raw[ctr])
			if i == -1:
				continue
			else:
				bow.addWord(str(i))
				del raw[ctr]

		for ctr in range(len(bow.words)):
			out += bow.words[ctr].word + ":" + str(bow.words[ctr].count) + " "

		return out + "\n"
