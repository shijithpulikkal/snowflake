import requests
import pandas as pd
from snowflake.snowpark import Session

connection_params = {
    "account": "XXXXXXXX",
    "user": "XXXXXXX",
    "password": "XXXXXXX",
    "role": "ACCOUNTADMIN",
    "warehouse": "DBT_WH",
    "database": "DBT_DEMO",
    "schema": "RAW"
}

session = Session.builder.configs(connection_params).create()

response = requests.get(
    "https://api.exchangerate-api.com/v4/latest/USD"
)

data = response.json()

rates_df = pd.DataFrame(
    list(data["rates"].items()),
    columns=["currency_code", "rate_to_usd"]
)

rates_df["base_date"] = data["date"]

snow_df = session.create_dataframe(rates_df)

snow_df.write.mode("overwrite").save_as_table(
    "RAW.EXCHANGE_RATES_RAW"
)

print(
    session.table(
        "RAW.EXCHANGE_RATES_RAW"
    ).count()
)