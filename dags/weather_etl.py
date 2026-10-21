import dlt

from weather_source import weather_hourly


def run():

    pipeline = dlt.pipeline(
        pipeline_name="weather_pipeline",
        destination=dlt.destinations.postgres(
        credentials={
            "host": "postgres",
            "port": 5432,
            "database": "airflow",
            "username": "airflow",
            "password": "airflow"
        }
    )
    )

    load_info = pipeline.run(
        weather_hourly()
    )

    print(load_info)