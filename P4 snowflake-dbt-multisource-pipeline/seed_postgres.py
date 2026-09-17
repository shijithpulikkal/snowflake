import psycopg2
from faker import Faker
import random

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="postgres"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id SERIAL PRIMARY KEY,
        customer_id VARCHAR(20),
        issue_type VARCHAR(50),
        status VARCHAR(20),
        created_at TIMESTAMP
    )
""")

issue_types = [
    "shipping_delay",
    "product_defect",
    "billing_issue",
    "return_request",
    "other"
]

statuses = [
    "open",
    "resolved",
    "escalated"
]

for _ in range(500):
    cur.execute(
        """
        INSERT INTO support_tickets
        (customer_id, issue_type, status, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (
            f"CUST-{random.randint(1000,9999)}",
            random.choice(issue_types),
            random.choice(statuses),
            fake.date_time_this_year()
        )
    )

conn.commit()

cur.close()
conn.close()

print("Seeded 500 support tickets")