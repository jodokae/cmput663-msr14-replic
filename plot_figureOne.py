import pymysql
import numpy
import matplotlib.pyplot as plt

figure_one_query = 'select projects.name, AVG(commit_sentiment.sentiment) \
FROM commit_comments \
INNER JOIN commits ON commits.id = commit_comments.commit_id \
INNER JOIN projects on projects.id = commits.project_id \
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id \
WHERE projects.name LIKE \'Jquery\' OR projects.name LIKE \'Rails\' OR projects.name LIKE \'CraftBukkit\' OR \
projects.name LIKE \'Diaspora\' OR projects.name LIKE \'MaNGOS\' OR projects.name LIKE \'TrinityCore\' \
GROUP BY projects.name;'

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor()
numrows = curs.execute(figure_one_query)

name = []
value = []
A = [row for row in curs]
for item in A:
    name.append(item[0])
    value.append(float(item[1]))
print(name)
print(value)

y_pos = numpy.arange(len(name))

plt.bar(y_pos, value)
plt.xticks(y_pos, name)
plt.show()
