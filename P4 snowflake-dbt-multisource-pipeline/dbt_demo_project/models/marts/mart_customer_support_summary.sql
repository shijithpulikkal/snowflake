SELECT
    t.customer_id,
    COUNT(*) AS total_tickets,

    SUM(
        CASE
            WHEN t.status = 'open'
            THEN 1
            ELSE 0
        END
    ) AS open_tickets,

    SUM(
        CASE
            WHEN t.status = 'escalated'
            THEN 1
            ELSE 0
        END
    ) AS escalated_tickets,

    COALESCE(
        SUM(o.sales_amount_usd),
        0
    ) AS lifetime_value_usd

FROM {{ ref('stg_support_tickets') }} t

LEFT JOIN {{ ref('fct_orders') }} o
       ON t.customer_id = o.customer_id

GROUP BY t.customer_id