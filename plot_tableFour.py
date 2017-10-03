import pymysql
import numpy
import matplotlib.pyplot as plt
from prettytable import PrettyTable

table_four_query = 'select daytime,count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment) \
from commit_comments \
inner join commit_sentiment on commit_comments.id = commit_sentiment.id \
group by daytime \
HAVING COUNT(commit_comments.id) > 200'

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor() #Use a client side cursor so you can access curs.rowcount
numrows = curs.execute(table_four_query)

times = ['Morning', 'Afternoon', 'Evening', 'Night']

t = PrettyTable(['Time of Day', 'Commits', 'Mean', 'Stand. Dev.'])
A = [row for row in curs]
for item in A:
    t.add_row([times[item[0]], item[1], item[2], item[3]])
    
print(t)
