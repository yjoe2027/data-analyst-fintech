-- mart/dim_condition.sql
with conditions as (
    select distinct condition_category
    from {{ ref('stg_weather') }}
),

enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['condition_category']) }}  as condition_key,
        condition_category,
        case condition_category
            when 'Clear'   then 'Sunny or clear skies'
            when 'Cloudy'  then 'Overcast or partly cloudy'
            when 'Rainy'   then 'Rain or drizzle'
            when 'Snowy'   then 'Snow or blizzard'
            when 'Foggy'   then 'Fog or mist'
            when 'Stormy'  then 'Thunderstorm or severe weather'
            else 'Mixed or unclassified conditions'
        end                                                              as example_condition_text,
        case condition_category
            when 'Clear'   then 'Positive'
            when 'Cloudy'  then 'Slightly Negative'
            when 'Rainy'   then 'Negative'
            when 'Snowy'   then 'Negative'
            when 'Foggy'   then 'Neutral'
            when 'Stormy'  then 'Very Negative'
            else 'Neutral'
        end                                                              as market_sentiment_bias,
        case condition_category
            when 'Clear'   then 5
            when 'Cloudy'  then 3
            when 'Rainy'   then 2
            when 'Snowy'   then 2
            when 'Foggy'   then 3
            when 'Stormy'  then 1
            else 3
        end                                                              as trading_activity_score
    from conditions
)

select * from enriched
