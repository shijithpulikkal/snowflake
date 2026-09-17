SELECT
    order_id,
    customer_id,
    customer_name,
    order_date,
    sales_amount,
    sales_amount AS sales_amount_usd
FROM {{ ref('stg_orders') }}