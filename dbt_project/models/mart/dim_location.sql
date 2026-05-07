-- mart/dim_location.sql
with locations as (
    select distinct
        location_name,
        region,
        country,
        lat,
        lon
    from {{ ref('stg_weather') }}
),

enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['location_name']) }}  as location_key,
        location_name,
        region,
        country,
        lat,
        lon,
        case location_name
            when 'New York'       then 'NYSE / NASDAQ'
            when 'London'         then 'LSE'
            when 'San Francisco'  then 'NASDAQ'
            else 'Other'
        end                                                         as financial_market,
        case location_name
            when 'New York'       then 'America/New_York'
            when 'London'         then 'Europe/London'
            when 'San Francisco'  then 'America/Los_Angeles'
            else 'UTC'
        end                                                         as timezone,
        case location_name
            when 'New York'       then 'USD'
            when 'London'         then 'GBP'
            when 'San Francisco'  then 'USD'
            else 'USD'
        end                                                         as primary_currency
    from locations
)

select * from enriched
