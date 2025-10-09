from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# SYNC Endpoint
@app.get("/sync-task-new")
def sync_task1():
    time.sleep(5) # blocking
    sync_task2()
    return {"Message" : "Sync Task 1 & 2 completed after 10 seconds"}

def sync_task2():
    time.sleep(5) # blocking
    return None