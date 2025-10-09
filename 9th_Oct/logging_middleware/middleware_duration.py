from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import time
import traceback
import asyncio

app = FastAPI()

# ---------------- SETUP STRUCTURED LOGGING ----------------
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

# MIDDLEWARE - Finding Duration for each request to run
@app.middleware("http")
async def get_duration_from_request(request: Request, call_next):
    start = time.time()
    response = await call_next(request)

    duration = time.time() - start
    logging.info(f"Duration: {duration:.4f} seconds")
    response.headers["Req_Duration"] = str(duration)
    return response

# ROUTES
students = [{"id": 1, "name": "Rahul"}, {"id": 2, "name": "Neha"}]

@app.get("/students")
async def get_students():
    logging.info("Fetching all students from database...")
    await asyncio.sleep(5)
    return students