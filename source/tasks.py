import asyncio
import uvloop

from celery.exceptions import SoftTimeLimitExceeded
from source import celery_logger as logger, uv_event
from source.celery_app import celery_app

asyncio.set_event_loop_policy(uv_event)


@celery_app.task(queue="start_ws", soft_time_limit=60 * 60)
def listen_ws():
    logger.info("Starting the listen_ws task")
    try:
        # This is where we would put the code to listen to the websocket
        # and save the data to the database
        pass
    except SoftTimeLimitExceeded:
        logger.info("The listen_ws task was stopped due to a soft time limit")
    finally:
        logger.info("Stopping the listen_ws task")


@celery_app.task(queue="default")
def regular_task():
    logger.info("Starting the regular_task")
