import pymysql
import numpy
import matplotlib.pyplot as plt
from prettytable import PrettyTable

table_two_query = 'SELECT projects.language, COUNT( commit_comments.id), AVG(commit_sentiment.sentiment), STD(commit_sentiment.sentiment) \
FROM commit_comments \
INNER JOIN commits on commit_comments.commit_id = commits.id \
INNER JOIN projects on commits.project_id = projects.id \
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id \
where projects.language like \'C\' or projects.language like \'C++\' or projects.language like \'Java\' or projects.language like \'Python\' or projects.language like \'Ruby\' \
GROUP BY projects.language'

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor() #Use a client side cursor so you can access curs.rowcount
numrows = curs.execute(table_two_query)

t = PrettyTable(['Language', 'Commits', 'Mean', 'Stand. Dev.'])
A = [row for row in curs]
for item in A:
    t.add_row([item[0], item[1], item[2], item[3]])
    
print(t)
