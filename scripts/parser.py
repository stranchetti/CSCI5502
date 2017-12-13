#!/usr/bin/env python3
import json
import gzip
import getpass
import argparse
import mysql.connector
import pickle

LENGTHS = {
    "event_id" : 30, #length of main id
    "url" : 256, #length of any url
    "login" : 64, #length of login names
    "ref" : 1024, #length of github refs
    "title" : 1024, #names of posts, repos, branches, etc.
}

#Base insertion statement
INSERT_BASE = (
    "insert into `%s`"
    "(%s)"
    "values (%s)"
)

#dictionary of table names mapped to tuple containing
#the schema of the table and an SQL statement that can
#be parameterized for inserting into the table
TABLES = {}

TABLES["actors"] = (
    (
        "`id` int not null,"
        "`login` TEXT not null,"
        "`gravatar_id` varchar(32),"
        "`avatar_url` varchar(" + str(LENGTHS["url"]) + "),"
        "`url` varchar(" + str(LENGTHS["url"]) + "),"
        "primary key (`id`)"
    ), INSERT_BASE % (
        "actors",
        "`id`, `login`, `gravatar_id`, `avatar_url`, `url`",
        "%s, %s, %s, %s, %s"
    )
)

TABLES["orgs"] = (
    (
        "`id` int not null,"
        "`login` TEXT not null,"
        "`gravatar_id` varchar(32),"
        "`avatar_url` varchar(" + str(LENGTHS["url"]) + "),"
        "`url` varchar(" + str(LENGTHS["url"]) + "),"
        "primary key (`id`)"
    ), INSERT_BASE % (
        "orgs",
        "`id`, `login`, `gravatar_id`, `avatar_url`, `url`",
        "%s, %s, %s, %s, %s"
    )
)

TABLES["repos"] = (
    (
        "`id` int not null,"
        "`name` varchar(" + str(LENGTHS["title"]) + ") not null,"
        "`url` varchar(" + str(LENGTHS["url"]) + "),"
        "primary key (`id`)"
    ), INSERT_BASE % (
        "repos",
        "`id`, `name`, `url`",
        "%s, %s, %s"
    )
)

TABLES["events"] = (
    (
        "`id` varchar(" + str(LENGTHS["event_id"]) + ") not null,"
        "`type` enum('CreateEvent', 'PushEvent', 'IssuesEvent',"
        "            'PullRequestEvent'),"
        "`repo` int not null,"
        "`actor` int not null,"
        "`org` int,"
        "`created` datetime not null,"
        "foreign key (`repo`) references `repos` (`id`),"
        "foreign key (`actor`) references `actors` (`id`),"
        "foreign key (`org`) references `org` (`id`),"
        "primary key (`id`)"
    ), INSERT_BASE % (
        "events",
        "`id`, `type`, `repo`, `actor`, `org`, `created`",
        "%s, %s, %s, %s, %s, %s"
    )
)

TABLES["create_events"] = (
    (
        "`id` varchar(" + str(LENGTHS["event_id"]) + ") not null,"
        "`ref` varchar(" + str(LENGTHS["ref"]) + "),"
        "`ref_type` enum ('branch', 'repository', 'tag') not null,"
        "`master_branch` varchar(" + str(LENGTHS["title"]) + "),"
        "`description` mediumtext,"
        "foreign key (`id`) references `events` (`id`)"
    ), INSERT_BASE % (
        "create_events",
        "`id`, `ref`, `ref_type`, `master_branch`, `description`",
        "%s, %s, %s, %s, %s"
    )
)

TABLES["push_events"] = (
    (
        "`id` varchar(" + str(LENGTHS["event_id"]) + ") not null,"
        "`push_id` int not null,"
        "`ref` varchar(" + str(LENGTHS["ref"]) + "),"
        "`head` char(40) not null,"
        "`before` char(40) not null,"
        "`size` int not null,"
        "`distinct` int not null,"
        "foreign key (`id`) references `events` (`id`),"
        "primary key (`push_id`)"
    ), INSERT_BASE % (
        "push_events",
        "`id`, `push_id`, `ref`, `head`, `before`, `size`, `distinct`",
        "%s, %s, %s, %s, %s, %s, %s"
    )
)

TABLES["commits"] = (
    (
        "`push_id` int not null,"
        "`sha` char(40) not null,"
        "`author` TEXT,"
        "`message` mediumtext,"
        "`message_length` int,"
        "`url` varchar(" + str(LENGTHS["url"]) + "),"
        "foreign key (`push_id`) references `push_events` (`push_id`)"
    ), INSERT_BASE % (
        "commits",
        "`push_id`, `sha`, `author`, `message`, `message_length`,`url`",
        "%s, %s, %s, %s, %s, %s"
    )
)

TABLES["issues_events"] = (
    (
        "`id` varchar(" + str(LENGTHS["event_id"]) + ") not null,"
        "`action` enum('opened', 'closed', 'reopened',"
        "              'assigned', 'unassigned',"
        "              'labeled', 'unlabeled',"
        "              'milestoned', 'demilestoned',"
        "              'edited') not null,"
        "`issue_id` int not null,"
        "`number` int not null,"
        "`title` varchar(" + str(LENGTHS["title"]) + "),"
        "`url` varchar(" + str(LENGTHS["url"]) + "),"
        "`user` int not null,"
        "`comments` int,"
        "`body` mediumtext,"
        "foreign key (`id`) references `events` (`id`),"
        "foreign key (`user`) references `actors` (`id`),"
        "primary key (`id`)"
    ), INSERT_BASE % (
        "issues_events",
        "`id`, `action`, `issue_id`, `number`, `title`, `url`, `user`, `comments`, `body`",
        "%s, %s, %s, %s, %s, %s, %s, %s, %s"
    )
)

TABLES["pull_request_events"] = (
    (
        "`id` varchar(" + str(LENGTHS["event_id"]) + ") not null,"
        "`action` enum('assigned', 'unassigned',"
        "              'review_requested', 'review_request_removed',"
        "              'labeled', 'unlabeled',"
        "              'opened', 'closed', 'reopened',"
        "              'edited') not null,"
        "`number` int not null,"
        "`request_id` int not null,"
        "`title` varchar(" + str(LENGTHS["title"]) + "),"
        "`body` mediumtext,"
        "`merged` bool,"
        "`internal_merge` bool,"
        "`commits` int,"
        "`additions` int,"
        "`modifications` int,"
        "`deletions` int,"
        "foreign key (`id`) references `events` (`id`),"
        "primary key (`id`)"
    ), INSERT_BASE % (
        "pull_request_events",
        "`id`, `action`, `number`, `request_id`, `title`, `body`, `merged`, `internal_merge`, `commits`, `additions`, `modifications`, `deletions`",
        "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    )
)

#load events from a .json.gz file
def load_json_file(file_name):
    with gzip.open(file_name, "rb") as f:
        data_bytes = f.read()
    #files are in bytes. unfortunately
    #python3 json module doesn't support
    #bytes natively until 3.6, so i'm
    #converting to strings
    data_strings = data_bytes.decode("utf-8")
    data = []
    for event in data_strings.split("\n"):
        #files end in a newline, leading to
        #an empty string
        if event != "":
            data.append(json.loads(event))
    return data

#insert event into database
def insert_event(cursor, event, repo_hash):
    if repo_hash is not None:
        if not repo_hash.get(str(event["repo"]["id"])):
            #ignore this event if it isn't on a repo we
            #are interested in
            return
    event_id = event["id"]
    event_type = event["type"]
    event_org = event.get("org", None)
    event_time = event["created_at"]
    #split payload handling based on event type
    if event_type == "CreateEvent":
        _insert_create_event(cursor, event["payload"], event_id)
    elif event_type == "PushEvent":
        _insert_push_event(cursor, event["payload"], event_id)
    elif event_type == "IssuesEvent":
        _insert_issues_event(cursor, event["payload"], event_id)
    elif event_type == "PullRequestEvent":
        _insert_pull_request_event(cursor, event["payload"], event_id)
    else:
        #this event isn't one we care about
        return
    actor_id = _insert_actor(cursor, event["actor"])
    repo_id = _insert_repo(cursor, event["repo"])
    org_id = None
    if event_org is not None:
        org_id = _insert_org(cursor, event_org)
    new_event = (event_id,
                 event_type,
                 repo_id,
                 actor_id,
                 org_id,
                 event_time.replace("T", " ").replace("Z", ""))
    #cursor.execute(TABLES["events"][1], new_event)
    _execute_insert(cursor, "events", new_event)

#inserts a create event into database
def _insert_create_event(cursor, payload, event_id):
    ref = payload["ref"]
    ref_type = payload["ref_type"]
    master_branch = payload["master_branch"]
    desc = payload["description"]
    new_create = (event_id,
                  ref,
                  ref_type,
                  master_branch,
                  desc)
    _execute_insert(cursor, "create_events", new_create)

#inserts a push event into database
def _insert_push_event(cursor, payload, event_id):
    push_id = payload["push_id"]
    ref = payload["ref"]
    head = payload["head"]
    before = payload["before"]
    size = payload["size"]
    distinct = payload["distinct_size"]
    new_push = (event_id,
                push_id,
                ref,
                head,
                before,
                size,
                distinct)
    _insert_commits(cursor, payload["commits"], push_id)
    _execute_insert(cursor, "push_events", new_push)

#insert issue event into database
def _insert_issues_event(cursor, payload, event_id):
    action = payload["action"]
    issue_id = payload["issue"]["id"]
    number = payload["issue"]["number"]
    title = payload["issue"]["title"]
    url = payload["issue"]["url"]
    user = payload["issue"]["user"]["id"]
    comments = payload["issue"]["comments"]
    body = payload["issue"]["body"]
    new_issue = (event_id,
                 action,
                 issue_id,
                 number,
                 title,
                 url,
                 user,
                 comments,
                 body)
    _execute_insert(cursor, "issues_events", new_issue)

#insert pull request event into database
def _insert_pull_request_event(cursor, payload, event_id):
    req = payload["pull_request"]
    
    action = payload["action"]
    number = payload["number"]
    request_id = req["id"]
    title = req["title"]
    body = req["body"]
    merged = req["merged"]
    #somehow, the repo field in the head and base
    #can be null, so we need a check to avoid
    #getting errors
    head_id = req["head"]["repo"]
    if head_id is not None:
        head_id = head_id.get("id", None)
    base_id = req["base"]["repo"]
    if base_id is not None:
        base_id = base_id.get("id", None)
    commits = req["commits"]
    adds = req["additions"]
    mods = req["changed_files"]
    dels = req["deletions"]
    #propagate NULL thorugh to the final value
    internal = None
    if head_id is not None and base_id is not None:
        internal = (head_id == base_id)
    
    new_request = (event_id,
                   action,
                   number,
                   request_id,
                   title,
                   body,
                   merged,
                   internal,
                   commits,
                   adds,
                   mods,
                   dels)
    _execute_insert(cursor, "pull_request_events", new_request)

#insert actor into database
def _insert_actor(cursor, actor):
    actor_id = actor["id"]
    actor_login = actor["login"]
    actor_gravatar = actor["gravatar_id"]
    actor_avatar = actor["avatar_url"]
    actor_url = actor["url"]
    new_actor = (actor_id,
                 actor_login,
                 actor_gravatar,
                 actor_avatar,
                 actor_url)
    _execute_insert(cursor, "actors", new_actor)
    return actor_id

#insert repo into database
def _insert_repo(cursor, repo):
    repo_id = repo["id"]
    repo_name = repo["name"]
    repo_url = repo["url"]
    new_repo = (repo_id,
                repo_name,
                repo_url)
    _execute_insert(cursor, "repos", new_repo)
    return repo_id

#insert org into database
def _insert_org(cursor, org):
    org_id = org["id"]
    org_login = org["login"]
    org_gravatar = org["gravatar_id"]
    org_avatar = org["avatar_url"]
    org_url = org["url"]
    new_org = (org_id,
               org_login,
               org_gravatar,
               org_avatar,
               org_url)
    _execute_insert(cursor, "orgs", new_org)
    return org_id

#insert commits into database
def _insert_commits(cursor, commits, push_id):
    for commit in commits:
        sha = commit["sha"]
        author = commit["author"]["name"]
        message = commit["message"]
        url = commit["url"]
        new_commit = (push_id,
                      sha,
                      author,
                      message,
                      len(message),
                      url)
        _execute_insert(cursor, "commits", new_commit)

#perform an insert statement to the sepcified table using
#the params provided. Performs checking for duplicate entries
#and raises any exceptions that occur
def _execute_insert(cursor, table, params):
    statement = TABLES[table][1]
    try:
        cursor.execute(statement, params)
    except mysql.connector.Error as error:
        #duplicate entries are expected, since we're not
        #actually checking beforehand if an entry is already
        #in a table since that will get expensive.
        if error.errno != mysql.connector.errorcode.ER_DUP_ENTRY:
            print("Inserting data ", end="")
            print(params, end="")
            print(" with statement %s failed" % statement)
            raise

#handle arguments
parser = argparse.ArgumentParser(description="A parser that populates a MySQL database out of the .json.gz archives from githubarchive.org")
parser.add_argument("-u", "--user", help="The username for the MySQL client to use. Defaults to user running this script.", default=getpass.getuser())
parser.add_argument("-p", "--pass", help="Specify that you wish to provide a password for use with the MySQL database connection", action="store_true", dest="passwd")
parser.add_argument("-r", "--repos", help="Specify a pickle file containing a python dictionary of the repo ids you want to consider", default=None)
parser.add_argument("-d", "--database", help="Specify the database name to use", default="datamining")
parser.add_argument("files", help="The list of gzipped json files to process", nargs="+")
args = parser.parse_args()

repo_hash = None
if args.repos:
    with open(args.repos, "rb") as f:
        repo_hash = pickle.load(f)

#get password if user requests to use one
passwd = None
if args.passwd:
    passwd = getpass.getpass("Please enter password:")
    
#establish database connection
#we need to use utf8mb4 to allow 4 byte utf8 encodings (for things like emoji in
#various user supplied text) since MySQL's utf8 encoding is set at 3 bytes max
try:
    ctx = mysql.connector.connect(user=args.user, passwd=passwd, charset="utf8mb4")
except mysql.connector.Error as error:
    print("Establishing connection to MySQL server failed: %s" % error)
    exit(1)
print("Etablished connection to MySQL server")

#get cursor for later operations
cursor = ctx.cursor()

#create database if needed
try:
    cursor.execute("create database if not exists `%s` default character set 'utf8mb4'" % args.database)
    ctx.database = args.database
except mysql.connector.Error as error:
    print("Creating database failed: %s" % error)
    cursor.close()
    ctx.close()
    exit(1)

#create tables in databases if needed
try:
    #since we can't guarantee what order the tables are in
    #in the TABLES dictionary, we need to make sure that MySQL
    #won't complain about creating foreign keys to tables that
    #don't exist yet
    cursor.execute("set foreign_key_checks=0")
    for name, schema in TABLES.items():
        statement = "create table if not exists `%s` (%s)" % (name, schema[0])
        print(statement)
        cursor.execute(statement)
except mysql.connector.Error as error:
    print("Creating table failed: %s" % error)
    cursor.close()
    ctx.close()
    exit(1)

#load each file and add to database
for f in args.files:
    print("Parsing " + f + "...")
    for event in load_json_file(f):
        try:
            insert_event(cursor, event, repo_hash)
            ctx.commit()
        except mysql.connector.Error as error:
            print("Populating database with file %s failed: %s" % (f, error))
            ctx.rollback()
            cursor.close()
            ctx.close()
            exit(1)

#close our connection
cursor.close()
ctx.close()
