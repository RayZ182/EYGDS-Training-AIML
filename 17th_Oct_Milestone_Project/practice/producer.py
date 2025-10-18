import pika
import json
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue="visit_tasks")

    task = {
        "VisitID": "V008",
        "PatientID": "P003",
        "DoctorID": "D101",
        "Date": "2025-10-09",
        "Cost": 1000
    }

    # Publish Message to queue
    channel.basic_publish(
        exchange = '',
        routing_key= 'visit_tasks',
        body = json.dumps(task),
        # properties=pika.BasicProperties(delivery_mode=2) # for persistent messages
    )
    logging.info(f"Sent visit {task['VisitID']}")
    print("Task sent to queue: ", task)
    connection.close()
except Exception as e:
    logging.error(f"Failed to send visits: {str(e)}")