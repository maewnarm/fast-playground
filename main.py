import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.scheduler import app as app_rocketry

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = app_rocketry.session


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())
    asyncio.create_task(app_rocketry.serve())


@app.on_event("shutdown")
def shutdown_event():
    session.shut_down()


@app.get("/scheduler-task")
async def get_tasks():
    return session.tasks
