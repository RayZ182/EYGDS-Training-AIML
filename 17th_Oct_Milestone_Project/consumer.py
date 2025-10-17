import pika
import json
import time
import logging
import pandas as pd
from etl_file import process_visits

logging.basicConfig(
    filename='visit_consumer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

accumulated_visits = []

def callback(ch, method, properties, body):
    global accumulated_visits
    start_time = time.time()

    visit = json.loads(body)
    print(f"Received visit {visit['VisitID']}")
    accumulated_visits.append(visit)

    # Process batch after 5 visits (or change batch size)
    if len(accumulated_visits) >= 6:
        try:
            visits_df = pd.DataFrame(accumulated_visits)
            process_visits(visits_df)
            accumulated_visits.clear()
            logging.info("Batch processed successfully.")
        except Exception as e:
            logging.error(f"ETL processing failed: {e}")
            print(f"ETL processing failed: {e}")

    processing_time = time.time() - start_time
    logging.info(f"Processed visit {visit['VisitID']} in {processing_time:.2f} seconds")


channel.basic_consume(queue="visit_tasks", on_message_callback=callback, auto_ack=True)

print("Waiting for visit messages. Press CTRL+C to exit.")
channel.start_consuming()