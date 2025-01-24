import asyncio
import datetime
import websockets
import json

MESSAGE_QUEUE = asyncio.Queue(maxsize=5000000)  # Buffer for incoming messages

async def producer(websocket):
    """
    Continuously receives messages from the WebSocket and adds them to the queue.
    """
    async for message in websocket:
        try:
            await MESSAGE_QUEUE.put((message))  # Add message to the queue
        except Exception as exception:
            print(
                f"[{datetime.datetime.now()}]: An exception occurred when queueing wss response: {exception}"
            )

async def consumer():
    """
    Processes messages from the queue in batches for high performance.
    """
    while True:
        batch = []
        try:
            # Collect a batch of messages
            while len(batch) < 100:  # Batch size
                batch.append(await MESSAGE_QUEUE.get())

            # Process the batch
            await process_batch(batch)  # Replace with actual processing logic
        except Exception as e:
            print(f"[{datetime.datetime.now()}]: Error during processing: {e}")

async def connect_to_certstream():
    """
    Connects to the Certstream server and starts the producer.
    """
    url = "wss://certstream.calidog.io/"
    while True:
        try:
            print(f"[{datetime.datetime.now()}]: Connecting to Certstream...")
            async with websockets.connect(
                url, max_queue=50000, max_size=1048576
            ) as websocket:
                print(f"[{datetime.datetime.now()}]: Connected to Certstream!")
                # Start the producer here inside a gather
                await asyncio.gather(producer(websocket), consumer())
        except websockets.ConnectionClosedError as e:
            print(
                f"[{datetime.datetime.now()}]: Connection closed: {e}. Reconnecting..."
            )
            await asyncio.sleep(1)
        except Exception as e:
            print(f"[{datetime.datetime.now()}]: Unexpected error: {e}. Retrying...")
            await asyncio.sleep(5)

async def process_batch(batch):
    """
    Process a batch of messages asynchronously. Replace this with actual async I/O logic.
    """
    for message in batch:
        message = json.loads(message)
        # Apply your logic here for each certificate
        print(message)

async def main():
    await connect_to_certstream()

if __name__ == "__main__":
    asyncio.run(main())
