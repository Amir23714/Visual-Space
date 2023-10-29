from fastapi import FastAPI, Request, Response
from routers.user import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware
import time
from datetime import datetime

import logging


async def formRequestLog(request: Request, call_next):
    request_time = datetime.utcnow()
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    client_ip = request.client.host
    url = request.url
    path = request.url.path
    http_method = request.method
    status_code = response.status_code

    logging.info(
        f"Request time : {request_time} | Process time : {process_time} | Sender : {client_ip} | Url : {url} | Method : {http_method} | Status : {status_code}")

    return response


app = FastAPI()

logging.basicConfig(filename='logs/mainApp.log', level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, prefix="/api")


# @app.on_event("startup")
# async def startup_event():

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await formRequestLog(request, call_next)
    return response
