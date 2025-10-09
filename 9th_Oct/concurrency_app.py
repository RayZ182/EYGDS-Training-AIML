from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# SYNC Endpoint
@app.get("/sync-task")
def sync_task():
    time.sleep(10) # blocking
    return {"Message" : "Sync Task completed after 10 seconds"}

# ASYNC Endpoint
@app.get("/async-task")
async def async_task():
    await asyncio.sleep(10) # non-blocking
    return {"Message" : "Async Task completed after 10 seconds"}