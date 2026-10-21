CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS weather_hourly (
    forecast_timestamp TIMESTAMP PRIMARY KEY,
    rain_mm NUMERIC,
    loaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE metadata.pipeline_cursor (
    source_name VARCHAR(100),
    entity_name VARCHAR(100),
    cursor_value TIMESTAMP,
    updated_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (
        source_name,
        entity_name
    )
);

CREATE TABLE metadata.pipeline_run (
    run_id UUID PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),
    rows_loaded INT,
    source_name VARCHAR(100)
);