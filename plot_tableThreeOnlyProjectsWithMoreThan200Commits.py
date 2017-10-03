import pymysql
import numpy
import matplotlib.pyplot as plt
from prettytable import PrettyTable

table_three_query = 'select weekday(commit_comments.created_at),count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment) \
from commit_comments \
inner join commit_sentiment on commit_comments.id = commit_sentiment.id \
inner join commits on commit_comments.commit_id = commits.id \
inner join projects on projects.id = commits.project_id \
where projects.id in ( \
select projects.id \
from projects inner join commits on projects.id = commits.project_id \
group by projects.id  \
having count(commits.id) > 200 \
) \
group by weekday(created_at); '

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor() #Use a client side cursor so you can access curs.rowcount
numrows = curs.execute(table_three_query)

weekday = ['Monday', 'Tuesday', 'Wednessday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

t = PrettyTable(['Weekday', 'Commits', 'Mean', 'Stand. Dev.'])
A = [row for row in curs]
for item in A:
    t.add_row([weekday[item[0]], item[1], item[2], item[3]])
    
print(t)

