
from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.sensors.http import HttpSensor
from airflow.models import Variable

import boto3
import requests
import os
import json

api_url = "https://v3.football.api-sports.io"

# Serie A
league = 71

players = {
    'John Arias': 13708,
    'German Cano': 13523,
    'Nino': 10306,
    'Ganso': 10311,
    'Keno': 16847,
    'Martinelli': 280245,
    'Andre': 265784,
    'Fabio': 10080
}

@task(task_id="get_player_stats")
def get_player_stats(player):
    params = {'league': 71, 'season': 2023, 'team': 124, 'id': player}
    headers = {'x-rapidapi-key': Variable.get("soccer_api_key")}

    r = requests.get(
            api_url + "/players",
            params = params,
            headers = headers).json()

    print(r)

    # filling schema with player stats
    q = r['response'][0]['statistics'][0]

    payload = {
        'id': player,
        'name': r['response'][0]['player']['name'],
        'goals': q['goals']['total'],
        'assists': q['goals']['assists'],
        'tackles': q['tackles']['total'],
        'position': q['games']['position'],
        'matches': q['games']['appearences'],
        'weight': r['response'][0]['player']['weight'],
        'height': r['response'][0]['player']['height'],
        'nationality': r['response'][0]['player']['nationality']
    }

    return payload

@task(task_id="send_data_to_s3")
def send_data_to_aws(data, path):
    for d in data:
        s3 = boto3.client(
            's3',
            aws_access_key_id = Variable.get('ACCESS_KEY'),
            aws_secret_access_key = Variable.get('SECRET_KEY')
        )

        s3.put_object(
            Bucket='simple-pipeline-lucastassi',
            Body=json.dumps(d),
            Key= path + '/' + d['id'].lower() + '.json'
        )

with DAG(
    dag_id="player_consuming",
    start_date=datetime(2025, 4, 9)
    #schedule="@daily"
) as dag:

    # implement http sensor to keep make sure api is available
    is_api_available = HttpSensor(
        task_id="is_api_available",
        http_conn_id="api_soccer",
        endpoint="",
        response_check=lambda response: '"code":200' in response.text,
        poke_interval=5
    )

    x = get_player_stats.expand(player=list(players.values()))

    # batch airflow style
    send_data_to_aws(x, "players")

    is_api_available >> x

