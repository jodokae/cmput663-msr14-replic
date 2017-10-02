# cmput663-msr14-replic

# Dataset # 

Download mysql dataset http://ghtorrent.org/msr14.html

``` 
$ mysql -u root -p
mysql > create user 'msr14'@'localhost' identified by 'msr14';
mysql> create database msr14;
mysql> GRANT ALL PRIVILEGES ON msr14.* to msr14@'localhost';
mysql> flush privileges;
# Exit MySQL prompt
# PW: msr14

$ zcat msr14-mysql.gz |mysql -u msr14 -p msr14
$ mysql -u msr14 -p msr14

#TRY: 
mysql> select language,count(*) from projects where forked_from is null group by language;

#Example: My result was not exactly the same
+------------+----------+
| language   | count(*) |
+------------+----------+
| C          |       10 |
| C#         |        8 |
| C++        |        8 |
| CSS        |        3 |
| Go         |        1 |
| Java       |        8 |
| JavaScript |        9 |
| PHP        |        9 |
| Python     |       10 |
| R          |        4 |
| Ruby       |       10 |
| Scala      |        9 |
| TypeScript |        1 |
+------------+----------+
13 rows in set (0.01 sec)
```

http://ghtorrent.org/files/schema.pdf

# Senti Strength #

Get SentiStrength for Java (http://sentistrength.wlv.ac.uk/) For academic purpose for free if you write a mail to m (dot) thelwall (at) wlv.ac.uk

Test: 
```
$ java -jar SentiStrengthCom.jar sentidata SentiStrength_Data/ input testfile.txt
```

Output gets generated as txt

# Analysis #

1. Create table for sentiment
```
create table commit_sentiment(id int primary key, sentiment int);
alter table commit_sentiment add sentiment_type int;
alter table commit_comments add daytime int;
```
2. Run analysis.py
3. Get helping values
```
update commit_sentiment set sentiment_type = 0 where sentiment >= -1 && sentiment <= 1;
update commit_sentiment set sentiment_type = 1 where sentiment >= 1;
update commit_sentiment set sentiment_type = -1 where sentiment <= -1;

update commit_comments set daytime = 0 where hour(commit_comments.created_at) >= 6 && hour(commit_comments.created_at) < 12;
update commit_comments set daytime = 1 where hour(commit_comments.created_at) >= 12 && hour(commit_comments.created_at) < 18;
update commit_comments set daytime = 2 where hour(commit_comments.created_at) >= 18 && hour(commit_comments.created_at) < 23;
update commit_comments set daytime = 3 where hour(commit_comments.created_at) >= 23 || hour(commit_comments.created_at) < 6;

```

# Results # 

-- Figure 1
select projects.name, AVG(commit_sentiment.sentiment)
FROM commit_comments
INNER JOIN commits ON commits.id = commit_comments.commit_id
INNER JOIN projects on projects.id = commits.project_id
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id
WHERE projects.name LIKE 'Jquery' OR projects.name LIKE 'Rails' OR projects.name LIKE 'CraftBukkit' OR projects.name LIKE 'Diaspora' OR projects.name LIKE 'MaNGOS' OR projects.name LIKE 'TrinityCore'
GROUP BY projects.name;

-- Figure 2
select projects.name, commit_sentiment.sentiment_type, COUNT(commit_sentiment.sentiment_type)
FROM commit_comments
INNER JOIN commits ON commits.id = commit_comments.commit_id
INNER JOIN projects on projects.id = commits.project_id
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id
WHERE projects.name LIKE 'Jquery' OR projects.name LIKE 'Rails' OR projects.name LIKE 'CraftBukkit' OR projects.name LIKE 'Diaspora' OR projects.name LIKE 'MaNGOS' OR projects.name LIKE 'TrinityCore'
GROUP BY projects.name, commit_sentiment.sentiment_type;

-- Table 2
SELECT projects.language, COUNT( commit_comments.id), AVG(commit_sentiment.sentiment), STD(commit_sentiment.sentiment)
FROM commit_comments
INNER JOIN commits on commit_comments.commit_id = commits.id
INNER JOIN projects on commits.project_id = projects.id
INNER JOIN commit_sentiment on commit_sentiment.id = commit_comments.id
where projects.language like 'C' or projects.language like 'C++' or projects.language like 'Java' or projects.language like 'Python' or projects.language like 'Ruby'
GROUP BY projects.language

-- Table 3
select dayname(commit_comments.created_at),count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment)
from commit_comments 
inner join commit_sentiment on commit_comments.id = commit_sentiment.id 
group by dayname(created_at);

-- Table 4
select daytime,count(distinct commit_comments.id),avg(commit_sentiment.sentiment),std(commit_sentiment.sentiment)
from commit_comments 
inner join commit_sentiment on commit_comments.id = commit_sentiment.id 
group by daytime
