import pika
import json
import time
import logging
import os
import csv
import subprocess

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def add_visit(task):
    # Define the fieldnames based on your task structure
    fieldnames = ['VisitID', 'PatientID', 'DoctorID', 'Date', 'Cost']

    # Check if the file exists to determine if we need to write the header
    file_exists = os.path.exists('visits.csv')

    try:
        with open('visits.csv', 'a', newline= '') as visits_file:
            writer = csv.DictWriter(visits_file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(task)
        logging.info(f"Task {task['VisitID']} is added.")
        return True

    except FileNotFoundError:
        logging.error("visits.csv file not found.")

def run_etl():
    logging.info("ETL started.")
    try:
        result = subprocess.run(
            ['python', 'etl_file.py'],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("ETL process Completed")

    except subprocess.CalledProcessError as e:
        logging.error(e.stdout)
    except FileNotFoundError:
        logging.error("etl_file.py not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

def callback(ch, method, properties, body):
    try:
        start_time = time.time()
        task = json.loads(body)
        print(f"Received visit {task['VisitID']}")
        print(f"Full Visit Detail: {task}")

        if add_visit(task):
            run_etl()
            logging.info(f"ETL Process Finished in {time.time() - start_time} seconds.")
        else:
            logging.error("ETL Process Failed. Visit cannot be added")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='visit_tasks')

    channel.basic_consume(
            queue='visit_tasks',
            on_message_callback=callback,
            auto_ack= True
    )
    print("Waiting for messages. Press CTRL+C to exit.")
    channel.start_consuming()

except Exception as e:
    logging.error(f"An unexpected error occurred: {str(e)}")