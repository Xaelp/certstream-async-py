import asyncio
import websockets
import logging

URI = "wss://certstream.calidog.io/"

# Set up logging
logging.basicConfig(level=logging.DEBUG)


async def measure_frame_size():
    async with websockets.connect(URI) as websocket:
        response = await websocket.recv()  # Receive a response
        response_size = len(response)
        print(f"Received frame with size: {response_size} bytes")


async def main():
    await measure_frame_size()


asyncio.run(main())
