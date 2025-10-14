import queue
import threading
import time

# create thread safe queue
my_queue = queue.Queue(maxsize=10)

# Producer Func
def producer(q, num_items = 5):
    print(f"Producer Starting. Will create {num_items} tasks")
    for i in range(num_items):
        task = i + 1
        q.put(task)
        print(f"\nProducer put task {task} in the queue")
        time.sleep(1)

    q.put(None)
    print("Producer finished creating tasks")

# Consumer Func
def consumer(q):
    print("Consuming Starting")
    while True:
        task = q.get()

        if task is None:
            print("Consumer: Received Termination. Exiting")
            q.task_done()
            break

        print(f"Consumer Got task {task}")
        time.sleep(1)

        print(f"\nConsumer Finished task {task}")
        q.task_done()

if __name__ == "__main__":
    # create the threads
    producer_thread = threading.Thread(target = producer, args = (my_queue,))
    consumer_thread = threading.Thread(target = consumer, args = (my_queue,))

    # start the thread
    producer_thread.start()
    consumer_thread.start()

    # wait for producer to finish generating tasks
    producer_thread.join()

    # wait for consumer to process all task
    my_queue.join()

    # wait for consumer thread to exit
    consumer_thread.join()

    print("\nMain: All tasks finished. Program Completed")