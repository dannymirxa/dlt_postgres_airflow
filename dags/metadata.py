import psycopg2

def get_connection():
    return psycopg2.connect(
        host="postgres",
        port=5432,
        dbname="airflow",
        user="airflow",
        password="airflow",
    )

def get_cursor():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT cursor_value
        FROM metadata.pipeline_cursor
        WHERE source_name=%s
        AND entity_name=%s
        """,
        (
            "open_meteo",
            "weather_hourly"
        )
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return None


def update_cursor(max_timestamp):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO metadata.pipeline_cursor
        (
            source_name,
            entity_name,
            cursor_value
        )
        VALUES (%s,%s,%s)

        ON CONFLICT
        (
            source_name,
            entity_name
        )
        DO UPDATE
        SET
            cursor_value = EXCLUDED.cursor_value,
            updated_at = NOW()
        """,
        (
            "open_meteo",
            "weather_hourly",
            max_timestamp
        )
    )

    conn.commit()

    cur.close()
    conn.close()
