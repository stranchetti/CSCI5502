-- run as mysql -u ... -p <database> < commit_lengths.sql

SELECT `message_length` FROM `commits`
INNER JOIN `push_events` ON `commits`.`push_id` = `push_events`.`push_id`
INNER JOIN `events` ON `push_events`.`id` = `events`.`id`
INNER JOIN `repos` ON `events`.`repo` = `repos`.`id`
WHERE `repos`.`success` = TRUE
INTO OUTFILE '/var/lib/mysql-files/commit_lengths_succ';

SELECT `message_length` FROM `commits`
INNER JOIN `push_events` ON `commits`.`push_id` = `push_events`.`push_id`
INNER JOIN `events` ON `push_events`.`id` = `events`.`id`
INNER JOIN `repos` ON `events`.`repo` = `repos`.`id`
WHERE `repos`.`success` = FALSE
INTO OUTFILE '/var/lib/mysql-files/commit_lengths_fail';
