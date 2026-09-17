SELECT
    "currency_code" AS currency_code,
    "rate_to_usd"::FLOAT AS rate_to_usd,
    TO_DATE("base_date") AS rate_date
FROM {{ source('raw', 'exchange_rates_raw') }}