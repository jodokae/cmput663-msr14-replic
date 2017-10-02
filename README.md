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


add a column to commit_comments table, called sentiment
run senti.py. (put the jar file and the data beside of this file)
