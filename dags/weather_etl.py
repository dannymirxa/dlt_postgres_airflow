import uuid
import requests

from datetime import datetime

from metadata import get_connection, get_cursor, update_cursor
from config import API_URL


def run():

    run_id = str(uuid.uuid4())

    conn = get_connection()
    cur = conn.cursor()

    start_time = datetime.utcnow()

    cur.execute(
        """
        INSERT INTO metadata.pipeline_run
        (
            run_id,
            start_time,
            status,
            rows_loaded,
            source_name
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            run_id,
            start_time,
            "RUNNING",
            0,
            "open_meteo"
        )
    )

    conn.commit()

    response = requests.get(
        API_URL,
        timeout=30
    )

    response.raise_for_status()

    payload = response.json()

    times = payload["hourly"]["time"]
    rains = payload["hourly"]["rain"]

    last_cursor = get_cursor()

    rows_loaded = 0
    max_timestamp = None

    for ts, rain in zip(times, rains):

        ts_dt = datetime.fromisoformat(ts)

        if last_cursor and ts_dt <= last_cursor:
            continue

        cur.execute(
            """
            INSERT INTO weather_hourly
            (
                forecast_timestamp,
                rain_mm
            )
            VALUES (%s,%s)

            ON CONFLICT
            (
                forecast_timestamp
            )
            DO UPDATE
            SET rain_mm = EXCLUDED.rain_mm
            """,
            (
                ts_dt,
                rain
            )
        )

        rows_loaded += 1

        if max_timestamp is None:
            max_timestamp = ts_dt
        else:
            max_timestamp = max(max_timestamp, ts_dt)

    conn.commit()

    if max_timestamp:
        update_cursor(max_timestamp)

    end_time = datetime.utcnow()

    cur.execute(
        """
        UPDATE metadata.pipeline_run
        SET
            end_time=%s,
            status=%s,
            rows_loaded=%s
        WHERE run_id=%s
        """,
        (
            end_time,
            "SUCCESS",
            rows_loaded,
            run_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    print(
        f"Loaded {rows_loaded} rows"
    )