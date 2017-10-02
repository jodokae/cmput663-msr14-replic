# cmput663-msr14-replic

# Setup

##Database ##

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


## Senti Strength ##

Get SentiStrength for Java (http://sentistrength.wlv.ac.uk/) For academic purpose for free if you write a mail to m (dot) thelwall (at) wlv.ac.uk


The 'SentiStrength_Data/' folder as well as the SentiStrengthCom.jar file need to be in root folder of the python scripts.

# Analysis #

To get the results do the following for steps

1. Create table for sentiment (in MySQL)
```
create table commit_sentiment(id int primary key, sentiment int);
alter table commit_sentiment add sentiment_type int;
alter table commit_comments add daytime int;
```
2. Run analysis.py
3. Get auxiliary values (in MySQL)
```
update commit_sentiment set sentiment_type = 0 where sentiment >= -1 && sentiment <= 1;
update commit_sentiment set sentiment_type = 1 where sentiment >= 1;
update commit_sentiment set sentiment_type = -1 where sentiment <= -1;

update commit_comments set daytime = 0 where hour(commit_comments.created_at) >= 6 && hour(commit_comments.created_at) < 12;
update commit_comments set daytime = 1 where hour(commit_comments.created_at) >= 12 && hour(commit_comments.created_at) < 18;
update commit_comments set daytime = 2 where hour(commit_comments.created_at) >= 18 && hour(commit_comments.created_at) < 23;
update commit_comments set daytime = 3 where hour(commit_comments.created_at) >= 23 || hour(commit_comments.created_at) < 6;
```

4. Run plot_xy to get result
