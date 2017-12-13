# Run this file as mysql -u root -p datamining <branching_strategies.sql

create table branching_strategies_join_success as (select `repo`, `ref`, `created`, `success` from events join push_events on events.id = push_events.id join repos on repos.id = events.repo where success);
create table branching_strategies_join_fail as (select `repo`, `ref`, `created`, `success` from events join push_events on events.id = push_events.id join repos on repos.id = events.repo where not success);

# Get the number of branches pushed to by repo
select repo, count(distinct ref) as num_branches from branching_strategies_join_success group by repo into outfile "branching_strategies1_out_success";
select repo, count(distinct ref) as num_branches from branching_strategies_join_fail group by repo into outfile "branching_strategies1_out_fail";

# Get the number of push events to master by repo
select repo, count(*) as num_master_pushes from branching_strategies_join_success where ref = 'refs/heads/master' group by repo into outfile "branching_strategies2_out_success";
select repo, count(*) as num_master_pushes from branching_strategies_join_fail where ref = 'refs/heads/master' group by repo into outfile "branching_strategies2_out_fail";

# Get the number of push events total by repo
select repo, count(*) as num_master_pushes from branching_strategies_join_success group by repo into outfile "branching_strategies3_out_success";
select repo, count(*) as num_master_pushes from branching_strategies_join_fail group by repo into outfile "branching_strategies3_out_fail";

# Get diagram data.
select repo, ref, dayofyear(created), count(*) from branching_strategies_join_success group by repo, ref, dayofyear(created) into outfile "branching_strategies4_out_success";
select repo, ref, dayofyear(created), count(*) from branching_strategies_join_fail group by repo, ref, dayofyear(created) into outfile "branching_strategies4_out_fail";

drop table branching_strategies_join_success;
drop table branching_strategies_join_fail;

