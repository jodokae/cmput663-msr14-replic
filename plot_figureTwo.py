import pymysql
import numpy
import matplotlib.pyplot as plt

def sumzip(*items):
    return [sum(values) for values in zip(*items)]

figure_two_query = 'select projects.name, commit_sentiment.sentiment_type, COUNT(commit_sentiment.sentiment_type) \
FROM commit_comments \
INNER JOIN commits ON commits.id = commit_comments.commit_id \
INNER JOIN projects on projects.id = commits.project_id \
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id \
WHERE projects.name LIKE \'Jquery\' OR projects.name LIKE \'Rails\' OR projects.name LIKE \'CraftBukkit\' OR \
projects.name LIKE \'Diaspora\' OR projects.name LIKE \'MaNGOS\' OR projects.name LIKE \'TrinityCore\' \
GROUP BY projects.name, commit_sentiment.sentiment_type;'

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor() #Use a client side cursor so you can access curs.rowcount
numrows = curs.execute(figure_two_query)

#curs.fecthall() is the iterator as per Kieth's answer
#count=numrows means advance allocation
#dtype='i4,i4' means two columns, both 4 byte (32 bit) integers
#A = numpy.fromiter(curs.fetchall(), count=numrows, dtype=('str, float32'))
name = []
pos = []
neu = []
neg = []
A = [row for row in curs]
for ind, item in enumerate(A):
    if ind % 3 == 0:
        name.append(item[0])
    if float(item[1]) == -1:
        neg.append(item[2])
    if float(item[1]) == 0:
        neu.append(item[2])
    if float(item[1]) == 1:
        pos.append(item[2])
#print(name)
#print(neg)
#print(neu)
#print(pos)

for i in range(0,6):
    summ = pos[i] + neu[i] + neg[i]
    pos[i] = pos[i] / summ
    neu[i] = neu[i] / summ
    neg[i] = neg[i] / summ

print(pos)

width = 0.35

y_pos = numpy.arange(len(name))

p1 = plt.bar(y_pos, pos, width, color='#d62728')
p2 = plt.bar(y_pos, neu, width, bottom=pos)
p3 = plt.bar(y_pos, neg, width, bottom=list(map(sum, zip(pos, neu))))

plt.legend((p1[0], p2[0], p3[0]), ('Positive', 'Neutral', 'Negative'))


#plt.bar(y_pos, value)
plt.xticks(y_pos, name)
plt.show()

