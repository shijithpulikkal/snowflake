import psycopg2
import pandas as pd
from snowflake.snowpark import Session

conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password="postgres", dbname="postgres")
tickets_df = pd.read_sql("SELECT * FROM support_tickets", conn)
conn.close()

connection_params = {
    "account": "XXXXXXX",
    "user": "XXXXXXX",
    "password": "XXXXXXX",
    "role": "ACCOUNTADMIN",
    "warehouse": "DBT_WH",
    "database": "DBT_DEMO",
    "schema": "RAW"
}

session = Session.builder.configs(connection_params).create()  # reuse from Step 3
snow_df = session.create_dataframe(tickets_df)
snow_df.write.mode("overwrite").save_as_table("raw.support_tickets_raw")

print(session.table("raw.support_tickets_raw").count())