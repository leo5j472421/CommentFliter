import pymysql
from Comment import *
from Dictionary import *

print "Connecting..."
conn = pymysql.connect(host='140.135.10.186', user='joshua', passwd='hijoshua', db='joshua')	#ICE-CYCU Server
#conn = pymysql.connect(host='127.0.0.1', user='joshua', passwd='1234', db='youtube')			#Local Server
cur = conn.cursor()

dictionary = Dictionary()
dictionary.loadDictionary()

sql_command = "SELECT COUNT(*) FROM comment_2w"
cur.execute(sql_command)
i = int(cur.fetchone()[0])
totext = ""

for ctr in range(i):
	sql_command = "SELECT TF, comment FROM comment_2w WHERE id=" + str(ctr+1)
	print i - ctr
	cur.execute(sql_command)
	row = cur.fetchone()
	comment = Comment(row[1])
	if(row[0] == "FALSE"):
		comment.flag = "0"
	else:
		comment.flag = "1"
	text = comment.BagOfWords(dictionary)
	totext += text

with open("Output-bow.txt", "w") as text_file:
	text_file.write(totext)

cur.close()
conn.close()
