import asyncio
import datetime
import websockets
import json
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

MESSAGE_QUEUE = asyncio.Queue(maxsize=1000000)  # Buffer for incoming messages


async def producer(websocket):
    """
    Continuously receives messages from the WebSocket and adds them to the queue.
    """
    async for message in websocket:
        try:
            await MESSAGE_QUEUE.put((message))  # Add message to the queue
        except Exception as exception:
            print(
                f"[{datetime.datetime.now()}]: An exception occurred when queueing (queue size: {MESSAGE_QUEUE.qsize()}) wss response: {exception}"
            )


async def consumer():
    """
    Processes messages from the queue in batches for high performance.
    """
    while True:
        batch = []
        try:
            batch_size = max(min(100, MESSAGE_QUEUE.qsize()), 1)
            # Collect a batch of messages
            while len(batch) < batch_size:
                batch.append(await MESSAGE_QUEUE.get())

            # Process the batch asynchronously
            await process_batch(batch)
        except Exception as e:
            print(
                f"[{datetime.datetime.now()}]: Error during processing queued messages: {e}"
            )


async def connect_to_certstream():
    """
    Connects to the Certstream server and starts the producer.
    """
    url = "wss://certstream.calidog.io/"
    while True:
        try:
            print(f"[{datetime.datetime.now()}]: Connecting to Certstream...")
            async with (
                websockets.connect(
                    url,
                    max_queue=100000,  # Each frame is around 2KB so this gives room to store 100K certificates to be read (around 200 seconds of data)
                    max_size=1048576,  # Each certificate is about 2KB so 1 MB gives plenty of room for each message received
                    ping_timeout=5,  # This timeout is many times higher than average ping time for this wss, so anything higher is already too much and better to reconnect
                    close_timeout=1,  # This allows application to reconnect faster by not waiting for proper close handshake
                ) as websocket
            ):
                print(f"[{datetime.datetime.now()}]: Connected to Certstream!")
                # Start the producer and consumer async tasks
                await asyncio.gather(producer(websocket), consumer())
        except websockets.ConnectionClosedError as e:
            print(
                f"[{datetime.datetime.now()}]: Connection closed: {e}. Reconnecting..."
            )
        except Exception as e:
            print(f"[{datetime.datetime.now()}]: Unexpected error: {e}. Retrying...")


async def process_batch(messages):
    """
    Asynchronously process a single message.
    """
    try:
        for message in messages:
            data = json.loads(message)
            # Apply your processing logic here
            print(data)
    except json.JSONDecodeError as e:
        print(f"[{datetime.datetime.now()}]: JSON decode error: {e}")


async def main():
    await connect_to_certstream()


if __name__ == "__main__":
    uvloop.run(main())
