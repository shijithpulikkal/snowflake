from snowflake.snowpark import Session

connection_params = {
    "account": "XXXXXX-XXXXXX",
    "user": "SXXXXXXX",
    "password": "XXXXXXXX",
    "role": "ACCOUNTADMIN",
    "warehouse": "ml_wh",
    "database": "ml_demo",
    "schema": "ml"
}

session = Session.builder.configs(connection_params).create()
print(session.sql("SELECT CURRENT_WAREHOUSE()").collect())
session.add_packages("pandas", "numpy", "scikit-learn", "xgboost", "joblib", "cloudpickle", "scipy")



df = session.table("raw.churn_raw")

df.describe().show()

# Confirm the actual column types
df.schema

# TOTALCHARGES is already FLOAT with some NULLs (blanks got auto-converted on load)
# Drop rows where it's null instead of filtering/casting a string
df = df.filter(df["TOTALCHARGES"].is_not_null())

# Drop the customer ID - not predictive
df = df.drop("CUSTOMERID")

print(df.count())


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score

# Pull the cleaned Snowpark df to pandas - fine at this size

# Create the numeric label BEFORE pulling to pandas
df = df.with_column("CHURN_LABEL", (df["CHURN"] == "Yes").cast("int"))
df = df.drop("CHURN")

# Now pull to pandas
pdf = df.to_pandas()

categorical_cols = ["GENDER", "PARTNER", "DEPENDENTS", "PHONESERVICE",
                     "MULTIPLELINES", "INTERNETSERVICE", "ONLINESECURITY",
                     "ONLINEBACKUP", "DEVICEPROTECTION", "TECHSUPPORT",
                     "STREAMINGTV", "STREAMINGMOVIES", "CONTRACT",
                     "PAPERLESSBILLING", "PAYMENTMETHOD"]
numeric_cols = ["TENURE", "MONTHLYCHARGES", "TOTALCHARGES"]

X = pdf[categorical_cols + numeric_cols]
y = pdf["CHURN_LABEL"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(transformers=[
    ("ohe", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("scale", StandardScaler(), numeric_cols)
])

full_pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("model", XGBClassifier(eval_metric="logloss"))
])

full_pipeline.fit(X_train, y_train)

preds = full_pipeline.predict(X_test)
acc = accuracy_score(y_test, preds)
f1 = f1_score(y_test, preds)
print(f"Accuracy: {acc:.3f}, F1: {f1:.3f}")

from snowflake.ml.registry import Registry

reg = Registry(session=session, database_name="ml_demo", schema_name="ml")

model_ref = reg.log_model(
    full_pipeline,
    model_name="churn_predictor",
    version_name="v1",
    comment="XGBoost churn model (native sklearn pipeline) trained on Telco dataset",
    metrics={"accuracy": acc, "f1_score": f1},
    sample_input_data=X_train.head(100)
)

reg.show_models()