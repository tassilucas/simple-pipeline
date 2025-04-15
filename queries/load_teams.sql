CREATE TABLE airflow.teams_schema.teams_stats (
    id VARCHAR(255),
    name VARCHAR(255),
    q1 INTEGER,
    q2 INTEGER,
    q3 INTEGER,
    q4 INTEGER,
    q5 INTEGER,
    q6 INTEGER
)

COPY airflow.teams_schema.teams
FROM 's3://simple-pipeline-lucastassi/teams/fluminense.json'
IAM_ROLE 'arn:aws:iam::254794824794:role/owner_role' FORMAT AS JSON 'auto'
REGION AS 'us-east-1'

COPY airflow.teams_schema.teams_stats
FROM 's3://simple-pipeline-lucastassi/teams/stats/fluminense.json'
IAM_ROLE 'arn:aws:iam::254794824794:role/owner_role'
FORMAT AS JSON 'auto'
REGION AS 'us-east-1'
