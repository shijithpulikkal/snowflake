import pandas as pd
from faker import Faker
import random

fake = Faker()

departments = [
    "Cardiology",
    "Oncology",
    "Pediatrics",
    "Radiology"
]

rows = []

for i in range(2000):
    rows.append({
        "patient_id": f"PT-{1000+i}",
        "full_name": fake.name(),
        "ssn": fake.ssn(),
        "department": random.choice(departments),
        "diagnosis": fake.random_element(
            elements=(
                "Hypertension",
                "Type 2 Diabetes",
                "Asthma",
                "Fracture",
                "Migraine"
            )
        ),
        "treatment_cost": round(
            random.uniform(200, 15000),
            2
        ),
        "admitted_date": fake.date_this_year()
    })

df = pd.DataFrame(rows)

df.to_csv(
    "synthetic_patients.csv",
    index=False
)

print(df.head())
print("Rows:", len(df))