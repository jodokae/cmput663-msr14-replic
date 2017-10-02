import subprocess
import shlex
import os
import numpy as np
import copy

def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    #Modify the location of SentiStrength.jar and D:/SentiStrength_Data/ if necessary
    p = subprocess.Popen(shlex.split("java -jar SentiStrengthCom.jar stdin sentidata SentiStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    #Can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    #convert from byte
    stdout_text = stdout_byte.decode("utf-8") 
    #replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ")
    return stdout_text 
#An example to illustrate calling the process.
##################################################################################print(RateSentiment('I am bad'))
#The above is OK for one text but inefficient to repeatedly call for many texts. Try instead: 
#  either modify the above to submit a file
#  or modify the above to send multiple lines through multiple calls of p.communicate(b)


import pymysql
conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
cur = conn.cursor()
cur.execute('select id from commit_comments;')
idList = copy.copy(cur)
for commitID in idList:
	if True:
		id = commitID[0]
		cur.execute('select body from commit_comments where id = ' + str(id) + ';')
		bodyList = copy.copy(cur)

		body = [b[0].replace('\n', '').replace('\r', '') for b in bodyList][0]
		sentiment = RateSentiment(body)
		a, b = sentiment.split()
		c  = [int(a), int(b)]
		r = 2
		if np.abs(c[0]) > np.abs(c[1]):
			r = 0
		else:
			r = 1
		s = c[r]
		print(id)
		cur.execute('UPDATE commit_comments SET sentiment = ' + str(s) + ' WHERE id =  ' + str(id) + '')	

cur.close()
conn.commit()
conn.close()