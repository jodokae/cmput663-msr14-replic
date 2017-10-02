# cmput663-msr14-replic

This repository tries to replicate the results of the paper https://dl.acm.org/citation.cfm?id=2597118 . Since the SentiStrength version and the GitHub Dataset were not exactly equal the results differ from the published ones. 

Section 2.2 of the paper gave some difficulties because it was not absolutly clear how the authors extracted the sentiments for the commits. We understood it so that they gave to whole commit to the sentiment analysis tool and worked on the given snippets. But because the results of this analyse is different of what is explained in this section it is also possible that they extracted the snippets with the tool run the sentiment analysis sentence by sentence and put it then back together. But we assumed that this is very unlikely and just the results of the tool changed in the last three years. 

Hence, we have different results than in the paper, the sentiments are generally more positive. This is also due to the fact that they proposed that the negative result of the analysis needs to be 1.5 times higher before they interpret a commit as negative. 

In order to replicate our results follow the steps in section Setup and Analysis.

# Content #

The main part of the repository is the analysis.py. First it will query all commits of the msr14 challenge out of a MySQL database which has to be downloaded and installed as described in section Setup. For performance reasons all the commits will be written into a file of the format "[commitID] \n [commitMessage] \n \n \n". This file is given to the SentimentAnalysis tool which gives us another file. This file is then processed as described in the paper (take average of positive and negative sentiment of every snippet, then assign either negative value, positive value or 0 depending on the values). These values are then written into a new table in the database.

Via the plot_xy.py files it is possible to reproduce the tables 2, 3 and 4 and figures 1 and 2 of the paper. We did not reproduce the section 3.4 because it needs manual grouping of the projects and cannot be derived from the dataset itself but needs additional information and a lot of time. 


# Setup #

## Database ##

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
```

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
