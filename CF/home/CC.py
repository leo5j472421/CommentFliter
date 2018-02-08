
from Comment import *
from Dictionary import *


dictionary = Dictionary() 	# Collection of Words with frequency


for ctr in open('1.txt','r'):
  comment = Comment(ctr)
  dictionary.addWords(comment.tokenize())
#dictionary.words.sort()

with open("OOutput-stemmed.txt", "w") as text_file:
	for word in dictionary.words:
		#print word.word, word.count
		text_file.write(word.word + " " + str(word.count) + "\n")
