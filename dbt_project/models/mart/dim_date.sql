-- mart/dim_date.sql
with dates as (
    select distinct extraction_date as date_key
    from {{ ref('stg_weather') }}
    where extraction_date is not null
),

enriched as (
    select
        date_key,
        year(date_key)                                      as year,
        month(date_key)                                     as month,
        day(date_key)                                       as day,
        dayofweek(date_key)                                 as day_of_week,
        dayname(date_key)                                   as day_name,
        monthname(date_key)                                 as month_name,
        quarter(date_key)                                   as quarter,
        case when dayofweek(date_key) between 1 and 5
             then true else false end                       as is_weekday,
        case when dayofweek(date_key) in (0, 6)
             then true else false end                       as is_weekend
    from dates
)

select * from enriched
