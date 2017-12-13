# Run this file as mysql -u root -p datamining <branching_strategies.sql

# Get the number of branches pushed to by repo
select repo, count(distinct ref) as num_branches from (select events.`id`, `type`, `repo`, `actor`, `org`, `created`, `push_id`, `ref`, `head`, `before`, `size`, `distinct` from events join push_events on events.id = push_events.id) t group by repo into outfile "branching_strategies1_out";

# Get the number of push events to master by repo
select repo, count(*) as num_master_pushes from (select events.`id`, `type`, `repo`, `actor`, `org`, `created`, `push_id`, `ref`, `head`, `before`, `size`, `distinct` from events join push_events on events.id = push_events.id) t where ref = 'refs/heads/master' group by repo into outfile "branching_strategies2_out";

# Get the number of push events total by repo
select repo, count(*) as num_master_pushes from (select events.`id`, `type`, `repo`, `actor`, `org`, `created`, `push_id`, `ref`, `head`, `before`, `size`, `distinct` from events join push_events on events.id = push_events.id) t group by repo into outfile "branching_strategies3_out";

# Get diagram data.
select repo, ref, dayofyear(created), count(*) from (select `repo`, `ref`, `created` from events join push_events on events.id = push_events.id) t group by repo, ref, dayofyear(created) limit 10 into outfile "branching_strategies4_out";

