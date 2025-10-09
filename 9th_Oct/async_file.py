from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# ASYNC Endpoint
@app.get("/async-task-new")
async def async_task1():
    await asyncio.sleep(5) # non-blocking
    return {"Message" : "Async Task 1 completed after 10 seconds"}

@app.get("/async-task-new")
async def async_task2():
    await asyncio.sleep(5) # non-blocking
    return {"Message" : "Async Task 2 completed after 10 seconds"}