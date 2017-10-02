
-- Figure 1
select projects.name, AVG(commit_comments.sentiment)
FROM commit_comments
INNER JOIN commits ON commits.id = commit_comments.commit_id
INNER JOIN projects on projects.id = commits.project_id
WHERE projects.name LIKE 'Jquery' OR projects.name LIKE 'Rails' OR projects.name LIKE 'CraftBukkit' OR projects.name LIKE 'Diaspora' OR projects.name LIKE 'MaNGOS' OR projects.name LIKE 'TrinityCore'
GROUP BY projects.name

-- Table 2
SELECT projects.language, COUNT( commit_comments.id), AVG(commit_comments.sentiment), STD(commit_comments.sentiment)
FROM commit_comments
INNER JOIN commits on commit_comments.commit_id = commits.id
INNER JOIN projects on commits.project_id = projects.id
where projects.language like 'C' or projects.language like 'C++' or projects.language like 'Java' or projects.language like 'Python' or projects.language like 'Ruby'
GROUP BY projects.language


-- Table 3
SELECT weekday(commits.created_at), COUNT(DISTINCT commit_comments.id), AVG(commit_comments.sentiment), STD(commit_comments.sentiment)
FROM commit_comments
INNER JOIN commits on commit_comments.commit_id = commits.id
GROUP BY weekday(commits.created_at)


-- Table 4
SELECT cut(commits.created_at, breaks= as.POSIXct(paste("2001-01-01",c("00:00:00", "06:00:00", "12:00:00","18:00:00","23:00:00","09:00:00")),format="%Y-%m-%d %H:%M:%S", tz ="Portugal"),labels=c('night','morning','Afternoon','Evening'))
, COUNT(DISTINCT commit_comments.id), AVG(commit_comments.sentiment), STD(commit_comments.sentiment)
FROM commit_comments
INNER JOIN commits on commit_comments.commit_id = commits.id
GROUP BY weekday(commits.created_at)


