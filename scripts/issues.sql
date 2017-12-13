CREATE TABLE issues_tmp AS
    (SELECT e.repo,e.created,r.success,i.* FROM repos r
    INNER JOIN events e on e.repo = r.id
    INNER JOIN issues_events i on i.id = e.id);

SELECT COUNT(*),repo,month(created) AS month,comments,IFNULL(CHAR_LENGTH(body),0) AS body, success
    FROM issues_tmp
    GROUP BY repo, month, success, body, comments
    INTO OUTFILE '/var/lib/mysql-files/issues_counts';

SELECT month(created) AS month,Count(*),sum(success=TRUE),sum(success=FALSE),sum(success=TRUE AND action='opened'),
    sum(success=FALSE AND action='opened'),sum(success=TRUE AND action='closed'),sum(success=FALSE AND action='closed'),
    sum(success=TRUE AND action='reopened'),sum(success=FALSE AND action='reopened')
    FROM issues_tmp
    GROUP BY month
    INTO OUTFILE '/var/lib/mysql-files/issues_type_counts';

DROP TABLE issues_tmp;
