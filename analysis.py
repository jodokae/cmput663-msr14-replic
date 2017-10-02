import numpy
import os
import pymysql
import time
import copy
import subprocess

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
cur = conn.cursor()
cur.execute('select id, body from commit_comments;')
idList = copy.copy(cur)
print('Preprocessing..')
f = open('senti_temp.txt', 'w')
for commitID in idList:
	if True:
		id = commitID[0]
		#cur.execute('select body from commit_comments where id = ' + str(id) + ';')
		#bodyList = copy.copy(cur)

		#body = [b[0].replace('\n', '').replace('\r', '') for b in commitID][1]
		body = commitID[1]

		#print(body)
		f.write(str(id))
		f.write('\n')
		f.write('\n')
		f.write(body)
		f.write('\n')
		f.write('\n')
		f.write('\n')
		f.write('\n')
f.close()
print('Sentiment Analysis ...')
subprocess.call(['java', '-jar', 'SentiStrengthCom.jar', 'sentidata', 'SentiStrength_Data/', 'input', 'senti_temp.txt'])
print('Calculating Sentiment and Writing to DB ..')
analysis = open('senti_temp0_out.txt', 'r')
lines = analysis.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
lines = [x.strip() for x in lines] 
lines.pop(0)
while len(lines) > 0:
	line = lines.pop(0)
	modLine = line.rstrip().replace("\t"," ")
	message = modLine[5:]
	
	if message == '':
		continue

	if message.isdigit():
		if lines[0].rstrip().replace("\t"," ")[5:] == '':
			lines.pop(0)
			maxPos = 0
			minNeg = 0
			snippetCount = 0;		
			while 1: 
				sentimentLine = lines.pop(0)
				modLine = sentimentLine.rstrip().replace("\t"," ")
				posSent = float(modLine[0:1])
				negSent = float(modLine[2:4])
				snippetCount = snippetCount + 1 
				lineMessage = modLine[5:]
				if lineMessage == '': 
					break
				maxPos = maxPos + posSent
				minNeg = minNeg + negSent
				#if posSent > maxPos:
				#	maxPos = posSent
				#if negSent < minNeg:
				#	minNeg = negSent
			maxPos = maxPos / snippetCount
			minNeg = minNeg / snippetCount
			finalSent = maxPos
			if numpy.abs(minNeg) > 1.5 * maxPos:
				finalSent = minNeg			
			if maxPos == 1 and minNeg == -1:
				finalSent = 0
			print(message + ':' + str(maxPos) + ', ' + str(minNeg) + ' Final: ' + str(finalSent))
			cur.execute('UPDATE commit_comments SET sentiment = ' + str(finalSent) + ' WHERE id =  ' + str(message) + '')
			
				
						

print('done')
f.close()
analysis.close()
os.remove('senti_temp.txt')
os.remove('senti_temp0_out.txt')
cur.close()
conn.commit()
conn.close()
