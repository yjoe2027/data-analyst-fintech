-- staging/stg_weather.sql
-- Cleans and standardizes raw WeatherAPI data

with source as (
    select * from {{ source('raw', 'weather_raw') }}
),

staged as (
    select
        id                                          as weather_id,
        trim(location_name)                         as location_name,
        trim(region)                                as region,
        trim(country)                               as country,
        lat,
        lon,
        temp_c,
        temp_f,
        round(temp_c, 1)                            as temp_c_rounded,
        trim(condition_text)                        as condition_text,

        -- Categorize weather condition
        case
            when lower(condition_text) like '%sun%'
              or lower(condition_text) like '%clear%'   then 'Clear'
            when lower(condition_text) like '%cloud%'
              or lower(condition_text) like '%overcast%' then 'Cloudy'
            when lower(condition_text) like '%rain%'
              or lower(condition_text) like '%drizzle%' then 'Rainy'
            when lower(condition_text) like '%snow%'
              or lower(condition_text) like '%blizzard%' then 'Snowy'
            when lower(condition_text) like '%fog%'
              or lower(condition_text) like '%mist%'    then 'Foggy'
            when lower(condition_text) like '%storm%'
              or lower(condition_text) like '%thunder%' then 'Stormy'
            else 'Other'
        end                                         as condition_category,

        wind_mph,
        wind_kph,
        humidity,
        feelslike_c,
        feelslike_f,
        uv,

        -- UV risk level
        case
            when uv < 3  then 'Low'
            when uv < 6  then 'Moderate'
            when uv < 8  then 'High'
            when uv < 11 then 'Very High'
            else 'Extreme'
        end                                         as uv_risk,

        -- Heat index comfort
        case
            when temp_c < 0   then 'Freezing'
            when temp_c < 10  then 'Cold'
            when temp_c < 18  then 'Cool'
            when temp_c < 24  then 'Comfortable'
            when temp_c < 30  then 'Warm'
            else 'Hot'
        end                                         as comfort_level,

        local_time,
        try_to_timestamp(local_time)                as local_timestamp,
        date(try_to_timestamp(local_time))          as local_date,
        hour(try_to_timestamp(local_time))          as local_hour,

        extracted_at,
        date(extracted_at)                          as extraction_date

    from source
    where location_name is not null
      and temp_c is not null
)

select * from staged
