# producer.py
import pika
import json
import pandas as pd

# Read visits CSV
visits = pd.read_csv("visits.csv")

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declare queue (idempotent)
channel.queue_declare(queue="visit_tasks")

# Push each visit row as JSON message
for _, row in visits.iterrows():
    visit_dict = row.to_dict()
    channel.basic_publish(
        exchange='',
        routing_key='visit_tasks',
        body=json.dumps(visit_dict)
    )
    print(f"Sent visit {visit_dict['VisitID']} to queue")

connection.close()
print("All visits sent to queue")