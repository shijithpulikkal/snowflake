SELECT DISTINCT
    customer_id,
    customer_name
FROM {{ ref('int_orders_usd') }}
