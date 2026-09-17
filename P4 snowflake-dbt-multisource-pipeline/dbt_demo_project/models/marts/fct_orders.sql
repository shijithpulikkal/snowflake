SELECT
    order_id,
    customer_id,
    order_date,
    sales_amount_usd
FROM {{ ref('int_orders_usd') }}