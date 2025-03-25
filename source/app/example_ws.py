import asyncio
import logging
from datetime import datetime
from websockets import ClientConnection
from websockets.exceptions import ConnectionClosedError
from websockets.asyncio.client import connect

from source.celery_app import celery_app

from source.settings import uri, uv_event, token

# Set the event loop policy to uvloop
asyncio.set_event_loop_policy(uv_event)


@celery_app.task(queue="default", soft_time_limit=60 * 60)
def take_message(message) -> None:
    """Process a message from the websocket."""
    # Process the message
    logging.info(f"Message: {message}")
    return None


async def send_message(websocket: ClientConnection, message: str) -> None:
    """Send a message to the websocket.

    Args:
        websocket: The websocket to send the message to.
        message: The message to send.
    """
    # Send the message to the websocket
    await websocket.send(message)


async def get_messages(websocket: ClientConnection) -> None:
    """Get messages from the websocket.

    Args:
        websocket: The websocket to get messages from.
    """
    # Get messages from the websocket
    await websocket.send("ping")
    await asyncio.sleep(0.1)
    async for message in websocket:
        # Process the message in the background, so that the websocket does not get blocked
        take_message.delay(message)


async def listen_chat() -> None:
    """Listen to the chat messages of a channel."""
    timeout = 60 * 29.58  # 29.58 minutes
    async for websocket in connect(
        uri=uri,
        max_queue=32,
        additional_headers=[("Authorization", token)],
    ):
        try:
            start_time = datetime.now()
            # Get messages from the websocket, with a timeout of 29.58 minutes
            await asyncio.wait_for(get_messages(websocket), timeout=timeout)
        except asyncio.TimeoutError:
            logging.info("TimeoutError in listen_chat")
            return None
        except ConnectionClosedError:
            logging.info("ConnectionClosedError in listen_chat")
            # Calculate the elapsed time
            elapsed_time = datetime.now() - start_time
            # Subtract the elapsed time from the timeout
            timeout = timeout - elapsed_time.total_seconds()
            continue
