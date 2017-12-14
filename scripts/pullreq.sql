SELECT `commits` FROM `pull_request_events`   INNER JOIN `events` ON `pull_request_events`.`id` = `events`.`id` INNER JOIN `repos` ON `events`.`repo` = `repos`.`id` WHERE `repos`.`success` = FALSE INTO OUTFILE '/var/lib/mysql-files/pullreq_commits_fail.txt';

SELECT `commits` FROM `pull_request_events`   INNER JOIN `events` ON `pull_request_events`.`id` = `events`.`id` INNER JOIN `repos` ON `events`.`repo` = `repos`.`id` WHERE `repos`.`success` = TRUE INTO OUTFILE '/var/lib/mysql-files/pullreq_commits_succ.txt';
