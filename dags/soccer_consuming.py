
from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.sensors.http import HttpSensor
from airflow.models import Variable

import requests
import os

api_url = "https://v3.football.api-sports.io"

# serie A
league = 71

players = {
    'John Arias': 79674,
    'German Cano': 13523,
    'Nino': 10306,
    'Ganso': 10311,
    'Keno': 16847,
    'Martinelli': 280245,
    'Andre': 265784,
    'Fabio': 10080
}

teams = {
    'Fluminense': 124
}

@task(task_id="get_team_goal_stats")
def get_team_goal_statistics():
    params = {'league': 71, 'season': 2023, 'team': 124}
    headers = {'x-rapidapi-key': Variable.get("soccer_api_key")}

    r = requests.get(
            api_url + "/teams/statistics",
            params = params,
            headers = headers).json()

    # filling schema scored_goals_distribution
    q = r['response']['goals']['for']['minute']

    payload = {
        'id': r['response']['team']['id'],
        'name': r['response']['team']['name'],
        'q1': q['0-15']['total'],
        'q2': q['16-30']['total'],
        'q3': q['31-45']['total'],
        'q4': q['46-60']['total'],
        'q5': q['61-75']['total'],
        'q6': q['76-90']['total'],
    }

@task(task_id="get_team_information")
def get_team_information():
    params = {'league': 71, 'season': 2023, 'team': 124}
    headers = {'x-rapidapi-key': Variable.get("soccer_api_key")}

    r = requests.get(
            api_url + "/teams/statistics",
            params = params,
            headers = headers).json()

    # filling schema teams_information
    payload = {
        'id': r['response']['team']['id'],
        'name': r['response']['team']['name'],
        'logo_url': r['response']['team']['logo'],
        'played_home': r['response']['fixtures']['played']['home'],
        'played_away': r['response']['fixtures']['played']['away'],
        'wins_home': r['response']['fixtures']['wins']['home'],
        'wins_away': r['response']['fixtures']['wins']['away'],
        'goals_for_home': r['response']['goals']['for']['total']['home'],
        'goals_for_away': r['response']['goals']['for']['total']['away'],
        'goals_against_home': r['response']['goals']['against']['total']['home'],
        'goals_against_away': r['response']['goals']['against']['total']['away'],
    }

with DAG(
    dag_id="soccer_consuming",
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

    is_api_available >> [get_team_information(), get_team_goal_statistics()]
