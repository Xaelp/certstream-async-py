import asyncio
import websockets
import time

URI = "wss://certstream.calidog.io/"


async def measure_latency():
    attempts = 5
    latency_times = []
    print(f"Testing round-trip latency over {attempts} attempts...")
    for _ in range(attempts):
        async with websockets.connect(URI) as websocket:
            # Send a ping frame and measure the time for the pong response
            start_time = time.monotonic()
            await websocket.ping()
            await websocket.recv()  # Wait for the pong response
            end_time = time.monotonic()

            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            latency_times.append(latency)
            await websocket.close()

    print(f"Statistics:")
    print(
        f"Average round-trip latency time: {sum(latency_times) / len(latency_times):.2f} ms"
    )
    print(f"Minimum round-trip latency time: {min(latency_times):.2f} ms")
    print(f"Maximum round-trip latency time: {max(latency_times):.2f} ms\n")


async def measure_connect_time():
    attempts = 5
    open_times = []
    print(f"Testing open connection time over {attempts} attempts...")
    for _ in range(attempts):
        try:
            start_time = time.monotonic()  # Start the timer
            async with websockets.connect(URI) as websocket:
                end_time = time.monotonic()  # Stop the timer once connected
                connect_time = (end_time - start_time) * 1000  # Convert to milliseconds
                open_times.append(connect_time)
                await websocket.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"Statistics:")
    print(f"Average open connection time: {sum(open_times) / len(open_times):.2f} ms")
    print(f"Minimum open connection time: {min(open_times):.2f} ms")
    print(f"Maximum open connection time: {max(open_times):.2f} ms\n")


async def measure_close_time():
    attempts = 5
    close_times = []
    print(f"Testing close connection time over {attempts} attempts...")
    for _ in range(attempts):
        try:
            async with websockets.connect(URI) as websocket:
                # Measure close connection time
                start_time = time.monotonic()  # Start timer
                await websocket.close()
                end_time = time.monotonic()  # Stop timer

                close_time = (end_time - start_time) * 1000  # Convert to milliseconds
                close_times.append(close_time)
        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"Statistics:")
    print(
        f"Average close connection time: {sum(close_times) / len(close_times):.2f} ms"
    )
    print(f"Minimum close connection time: {min(close_times):.2f} ms")
    print(f"Maximum close connection time: {max(close_times):.2f} ms\n")


asyncio.run(measure_latency())
asyncio.run(measure_connect_time())
asyncio.run(measure_close_time())
