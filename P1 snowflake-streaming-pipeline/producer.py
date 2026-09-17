import boto3, json, time, uuid
from datetime import datetime, timezone
from faker import Faker

fake = Faker()
s3 = boto3.client('s3')
BUCKET = 'shijithp-snowpipe-demo'

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": fake.random_int(min=1000, max=9999),
        "event_type": fake.random_element(elements=("click", "purchase", "view", "signup")),
        "value": round(fake.random.uniform(1, 500), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def push_batch(n=5):
    batch = [generate_event() for _ in range(n)]
    key = f"events/batch_{int(time.time())}.json"
    s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(batch))
    print(f"Pushed {n} events to {key}")

if __name__ == "__main__":
    while True:
        push_batch(n=5)
        time.sleep(10)