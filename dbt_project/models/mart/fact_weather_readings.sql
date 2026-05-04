-- mart/fact_weather_readings.sql
-- Fact table: one row per weather reading, joined to all dimensions

with stg as (
    select * from {{ ref('stg_weather') }}
),

dim_loc as (
    select * from {{ ref('dim_location') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

dim_cond as (
    select * from {{ ref('dim_condition') }}
),

fact as (
    select
        -- Surrogate key
        {{ dbt_utils.generate_surrogate_key(['s.weather_id']) }} as reading_key,

        -- Foreign keys
        dl.location_key,
        dd.date_key,
        dc.condition_key,

        -- Degenerate dimensions
        s.weather_id,
        s.local_timestamp,
        s.local_hour,
        s.extracted_at,

        -- Temperature measures
        s.temp_c,
        s.temp_f,
        s.temp_c_rounded,
        s.feelslike_c,
        s.feelslike_f,
        s.temp_c - s.feelslike_c                    as temp_feels_delta_c,

        -- Atmospheric measures
        s.humidity,
        s.uv,
        s.uv_risk,
        s.comfort_level,

        -- Wind measures
        s.wind_mph,
        s.wind_kph,

        -- Derived market-relevant metrics
        -- Comfort score: higher = better trading weather (proxy for sentiment)
        round(
            (case s.comfort_level
                when 'Comfortable' then 1.0
                when 'Warm'        then 0.8
                when 'Cool'        then 0.7
                when 'Cold'        then 0.4
                when 'Hot'         then 0.5
                when 'Freezing'    then 0.2
                else 0.5
            end
            * (1 - (s.humidity - 50) / 200.0)   -- penalize extreme humidity
            * (1 - s.wind_kph / 200.0))          -- penalize high wind
        , 3)                                        as weather_comfort_score,

        -- Flag extreme weather events
        case
            when s.wind_kph > 60
              or s.temp_c < -10
              or s.temp_c > 40
              or s.humidity > 90  then true
            else false
        end                                         as is_extreme_weather

    from stg s
    left join dim_loc  dl on s.location_name = dl.location_name
    left join dim_date dd on s.extraction_date = dd.date_key
    left join dim_cond dc on s.condition_category = dc.condition_category
)

select * from fact
