import pymysql
from Comment import *
from Dictionary import *

print "Connecting..."
conn = pymysql.connect(host='140.135.10.186', user='joshua', passwd='hijoshua', db='joshua')	#ICE-CYCU Server
#conn = pymysql.connect(host='127.0.0.1', user='joshua', passwd='1234', db='youtube')			#Local Server
cur = conn.cursor()

dictionary = Dictionary() 	# Collection of Words with frequency

sql_command = "SELECT COUNT(*) FROM comment_2w"
cur.execute(sql_command)
i = int(cur.fetchone()[0])

for ctr in range(i):
	sql_command = "SELECT comment FROM comment_2w WHERE id=" + str(ctr+1)
	print i - ctr
	cur.execute(sql_command)
	comment = Comment(cur.fetchone())
	dictionary.addWords(comment.tokenize())

cur.close()
conn.close()
dictionary.words.sort()

with open("Output-stemmed.txt", "w") as text_file:
	for word in dictionary.words:
		#print word.word, word.count
		text_file.write(word.word + " " + str(word.count) + "\n")
