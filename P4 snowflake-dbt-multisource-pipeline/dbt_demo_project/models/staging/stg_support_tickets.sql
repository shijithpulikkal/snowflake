SELECT
    "ticket_id" AS ticket_id,
    "customer_id" AS customer_id,
    "issue_type" AS issue_type,
    "status" AS status,
    "created_at" AS created_at
FROM {{ source('raw', 'support_tickets_raw') }}