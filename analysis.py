import numpy
import os
import pymysql
import time
import copy
import subprocess

def createAnalysisFile(commitList):
    f = open('senti_temp.txt', 'w')
    for commit in commitList:
        if True:
            id = commit[0]
            body = commit[1]

            f.write(str(id))
            f.write('\n')
            f.write('\n')
            f.write(body)
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
    f.close()

def analyse():
    commits = 0
    result = ''
    commitId = 0
    maxPos = 0
    minNeg = 0
    snippetCount = 0
    lastLineEmpty = False
    secondLastLineEmpty = False
    firstLine = True
    
    with open('senti_temp0_out.txt') as f:
        for line in f:
            modLine = line.rstrip().replace("\t"," ")
            message = modLine[5:]
                       
            if modLine == 'Positive Negative Text':
                firstLine = True
                print('Skipped first line')
                continue
            
            if message == '':
                if lastLineEmpty:
                    secondLastLineEmpty = True
                lastLineEmpty = True
                continue
		    
            if message.isdigit():
                if lastLineEmpty and secondLastLineEmpty and snippetCount > 0:
                    maxPos = maxPos / snippetCount
                    minNeg = minNeg / snippetCount
                    finalSent = maxPos
                    if numpy.abs(minNeg) > 1.5 * maxPos:
                        finalSent = minNeg			
                    if maxPos <= 1 and minNeg >= -1:
                        finalSent = 0
                    #print(str(commitId) + ':' + str(maxPos) + ', ' + str(minNeg) + ' Final: ' + str(finalSent))
                    if result != '':
                        result = result + ','
                    result = result + '(' + str(commitId) + ', ' + str(finalSent) + ')'
            
                    commitId = message
                    commits = commits + 1
                    maxPos = 0
                    minNeg = 0
                    snippetCount = 0
                    continue
                    
                if firstLine:
                    commitId = message
                    commits = commits + 1
                    maxPos = 0
                    minNeg = 0
                    snippetCount = 0
                    firstLine = False
                    continue
		    
            posSent = float(modLine[0:1])
            negSent = float(modLine[2:4])
            snippetCount = snippetCount + 1 
		    
            maxPos = maxPos + posSent
            minNeg = minNeg + negSent
            #if posSent > maxPos:
        	    #	maxPos = posSent
            #if negSent < minNeg:
        	    #	minNeg = negSent
        	
            lastLineEmpty = False
            secondLastLineEmpty = False
	
	#update last commit
    maxPos = maxPos / snippetCount
    minNeg = minNeg / snippetCount
    finalSent = maxPos
    if numpy.abs(minNeg) > 1.5 * maxPos:
        finalSent = minNeg			
    if maxPos == 1 and minNeg == -1:
        finalSent = 0
    #print(str(commitId) + ':' + str(maxPos) + ', ' + str(minNeg) + ' Final: ' + str(finalSent))
    if result != '':
        result = result + ','
    result = result + '(' + str(commitId) + ', ' + str(finalSent) + ')'
            
    return result
    

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
cur = conn.cursor()
cur.execute('select id, body from commit_comments;')
commitList = copy.copy(cur)

print('Preprocessing..')
createAnalysisFile(commitList)

print('Sentiment Analysis ...')
subprocess.call(['java', '-jar', 'SentiStrengthCom.jar', 'sentidata', 'SentiStrength_Data/', 'input', 'senti_temp.txt'])

print('Calculating Sentiment ..')
result = analyse()

print('Write to DB..')
cur.execute('INSERT INTO commit_sentiment(id,sentiment) VALUES ' + result + ' ON DUPLICATE KEY UPDATE id=VALUES(id),sentiment=VALUES(sentiment)')
                    		

print('done')
os.remove('senti_temp.txt')
os.remove('senti_temp0_out.txt')
cur.close()
conn.commit()
conn.close()
