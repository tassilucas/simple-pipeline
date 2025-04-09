
I like programming and soccer so, I decided to create this project as a way of learning more about
Data Engineering tools. This project is meant to be a practice experiment with the ETL orchestration
tool Apache Airflow that I have been studying for the past week. I will be developing a pipeline that
ingest, load and transform data from soccer matches (only Brazil) like goals, number of match played,
wins and etc. This data will be loaded in some Object Storage Service and retrieved from some BI tool.
Further details of data architecture and data modeling will be explained later.

1. Data ingestion:
    . API used: https://www.api-football.com/
    . This API gives the information needed in JSON format but has some limitations:
    	- Only 100 requests / day for free plan,
	  meaning the pipeline will be runned in limited daily batch
    . Some useful endpoints:
    	- /teams/statistics - information about team stats like wins, goals (home, away).
	- /players/statistics - information about player stats like goals, shots, games, photo, etc.
	- /leagues - information about leagues
    . Important to notice that we can filter using query parameters and get a relation about the data.
      For example, we want a specific player in a specific league from a specific team, because teams
      can play in more than one league and players also play for more than one team. This data is
      modeled using REST principles so it is not following the classical relational model.

1.1 Data ingestion storing:
    . Data should be ingested and stored in a Cloud Object Storage Service like GCS (Google Cloud Storage),
      then it will be later read and processed for being loaded in structured databases. So, in this step
      I will be making sure to correct store data retrieved by the previous step.
      	- Probabily will be using AWS S3 to get used to Amazon services.
	- This step is good to isolate tasks and also practice the multi node worker task processing.
	  Also, will be good to make as much as possible requests and later process it.

2. Data transform:
    . Transform step will use S3 Hooks/Operators built-in Airflow to retrieve only needed data.
    . Normalize data and check formats (date, lower/upper case, etc). Will perform only necessary checks
      exception handling since API is already guaranting the data quality.

3. Data loading:
    . The result data will be loaded in a cloud Data Warehouse.
    	. Probabily will be using Amazon Redshift to keep everything in same cloud provider.

4. Data architecture (?)
    . Still need to figure-out but probably
    	API-Football -> S3 -> Redshift or BigQuery -> Looker Studio (basic data visualization)
			<all tasks orchestrated by Apache Airflow>

5. Airflow deployment (?)
    . Docker
       . Can delay project end.
    . Local deployment with multiple workers (Celery) due to Cloud Costs (?)
    . Which more learned concepts of Airflow can we explore with this project?
    	- XCom
	- Sensors
	- Branch
