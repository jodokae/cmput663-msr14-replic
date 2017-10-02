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

figure_two_query = 'select projects.name, commit_sentiment.sentiment_type, COUNT(commit_sentiment.sentiment_type) \
FROM commit_comments \
INNER JOIN commits ON commits.id = commit_comments.commit_id \
INNER JOIN projects on projects.id = commits.project_id \
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id \
WHERE projects.name LIKE \'Jquery\' OR projects.name LIKE \'Rails\' OR projects.name LIKE \'CraftBukkit\' OR \
projects.name LIKE \'Diaspora\' OR projects.name LIKE \'MaNGOS\' OR projects.name LIKE \'TrinityCore\' \
GROUP BY projects.name, commit_sentiment.sentiment_type;'

table_two_query = 'SELECT projects.language, COUNT( commit_comments.id), AVG(commit_sentiment.sentiment), STD(commit_sentiment.sentiment) \
FROM commit_comments \
INNER JOIN commits on commit_comments.commit_id = commits.id \
INNER JOIN projects on commits.project_id = projects.id \
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id \
where projects.language like \'C\' or projects.language like \'C++\' or projects.language like \'Java\' or projects.language like \'Python\' or projects.language like \'Ruby\' \
GROUP BY projects.language'

table_three_query = 'select dayname(commit_comments.created_at),count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment) \
from commit_comments \
inner join commit_sentiment on commit_comments.id = commit_sentiment.id \
group by dayname(created_at);'

table_four_query = 'select daytime,count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment) \
from commit_comments \
inner join commit_sentiment on commit_comments.id = commit_sentiment.id \
group by daytime'

conn = pymysql.connect(host='localhost', user='msr14', passwd='msr14', db='msr14')
curs = conn.cursor() #Use a client side cursor so you can access curs.rowcount
numrows = curs.execute(table_two_query)

A = [row for row in curs]
for item in A:
    print(item)

