from airflow.sdk import dag, task
from datetime import datetime


@task
def load_weather():

    from weather_etl import run

    run()


@dag(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["weather"]
)
def weather_pipeline():
    load_weather()

weather_pipeline()