import os
import requests
import snowflake.connector
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

LOCATIONS = ["New York", "London", "San Francisco"]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS WEATHER_RAW (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    location_name VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100),
    lat FLOAT,
    lon FLOAT,
    temp_c FLOAT,
    temp_f FLOAT,
    condition_text VARCHAR(200),
    wind_mph FLOAT,
    wind_kph FLOAT,
    humidity INTEGER,
    feelslike_c FLOAT,
    feelslike_f FLOAT,
    uv FLOAT,
    local_time VARCHAR(50),
    extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
"""

INSERT_SQL = """
INSERT INTO WEATHER_RAW (
    location_name, region, country, lat, lon,
    temp_c, temp_f, condition_text, wind_mph, wind_kph,
    humidity, feelslike_c, feelslike_f, uv, local_time
) VALUES (
    %(location_name)s, %(region)s, %(country)s, %(lat)s, %(lon)s,
    %(temp_c)s, %(temp_f)s, %(condition_text)s, %(wind_mph)s, %(wind_kph)s,
    %(humidity)s, %(feelslike_c)s, %(feelslike_f)s, %(uv)s, %(local_time)s
)
"""


def fetch_weather(location: str) -> dict:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": os.environ["WEATHERAPI_KEY"], "q": location, "aqi": "no"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def parse_record(data: dict) -> dict:
    loc = data["location"]
    cur = data["current"]
    return {
        "location_name": loc["name"],
        "region": loc["region"],
        "country": loc["country"],
        "lat": loc["lat"],
        "lon": loc["lon"],
        "temp_c": cur["temp_c"],
        "temp_f": cur["temp_f"],
        "condition_text": cur["condition"]["text"],
        "wind_mph": cur["wind_mph"],
        "wind_kph": cur["wind_kph"],
        "humidity": cur["humidity"],
        "feelslike_c": cur["feelslike_c"],
        "feelslike_f": cur["feelslike_f"],
        "uv": cur["uv"],
        "local_time": loc["localtime"],
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }


def _snowflake_conn():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ.get("SNOWFLAKE_SCHEMA", "RAW"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ.get("SNOWFLAKE_ROLE"),
    )


def load_to_snowflake(records: list[dict]) -> None:
    conn = _snowflake_conn()
    cur = conn.cursor()
    try:
        cur.execute(CREATE_TABLE_SQL)
        for rec in records:
            cur.execute(INSERT_SQL, rec)
        conn.commit()
        print(f"Loaded {len(records)} records to WEATHER_RAW")
    finally:
        cur.close()
        conn.close()


def main():
    records = []
    for loc in LOCATIONS:
        print(f"Fetching weather for {loc}...")
        data = fetch_weather(loc)
        records.append(parse_record(data))
    load_to_snowflake(records)


if __name__ == "__main__":
    main()
