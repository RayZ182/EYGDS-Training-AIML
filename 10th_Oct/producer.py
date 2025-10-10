import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue
channel.queue_declare(queue = "student_tasks")

# prepare a message
task = {
    "student_id": 101,
    "action" : "generate_certificate",
    "email" : "rahul@example.com"
}

# Publish Message to queue
channel.basic_publish(
    exchange = '',
    routing_key= 'student_tasks',
    body = json.dumps(task)
)

print("Task sent to queue: ", task)
connection.close()