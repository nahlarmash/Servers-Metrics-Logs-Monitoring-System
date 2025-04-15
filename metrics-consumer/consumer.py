import os
import psycopg2
from kafka import KafkaConsumer
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
time.sleep(15)

consumer = KafkaConsumer(
    'test-topic4',
    bootstrap_servers=['kafka-1:9092', 'kafka-2:9093', 'kafka-3:9094'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: m.decode('utf-8'),
    group_id='metrics-consumer-group',
    enable_auto_commit=True
)

# Read DB credentials from environment variables
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'metricsdb')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    server_id TEXT,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    disk_usage FLOAT,
    timestamp TIMESTAMP
)
""")
conn.commit()

print("Metrics Consumer is running...")

for message in consumer:
    try:
        data = message.value
        print(f"Consumed: {data}")

        parts = dict(item.strip().split(": ") for item in data.split(","))
        server_id = parts.get("id")
        cpu = float(parts.get("cpu"))
        mem = float(parts.get("mem"))
        disk = float(parts.get("disk"))
        ts = datetime.utcnow()

        cursor.execute(
            "INSERT INTO metrics (server_id, cpu_usage, memory_usage, disk_usage, timestamp) VALUES (%s, %s, %s, %s, %s)",
            (server_id, cpu, mem, disk, ts)
        )
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
