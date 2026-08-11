import asyncio
import time
import httpx

URL = "http://127.0.0.1:8000/chat"

NUM_REQUESTS = 10

async def send_request(client, request_id):
    start_time = time.perf_counter()

    try:
        response = await client.post(
            URL,
            json = {
                "provider" : "groq",
                "prompt" : f"Load test request {request_id}"
            }
        )

        elapsed = time.perf_counter() - start_time

        print(
            f"Request {request_id} : "
            f"{response.status_code} "
            f" latency : {elapsed * 1000:.2f} ms " 
        )

    except Exception as e:
        elapsed = time.perf_counter() - start_time

        print(
            f"Request {request_id} : "
            f"ERROR "
            f" latency : {elapsed * 1000:.2f} ms "
            f"error: {type(e).__name__}: {e}"
        )

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:

        tasks = [
            send_request(client, i)
            for i in range(1, NUM_REQUESTS + 1)
        ]

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
