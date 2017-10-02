import pymysql
import numpy
import matplotlib.pyplot as plt

table_four_query = 'select daytime,count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment) \
from commit_comments \
inner join commit_sentiment on commit_comments.id = commit_sentiment.id \
group by daytime'

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor() #Use a client side cursor so you can access curs.rowcount
numrows = curs.execute(table_four_query)

A = [row for row in curs]
for item in A:
    print(item)

