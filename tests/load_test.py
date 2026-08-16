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
        data = response.json()
        cached = data.get("cached", False)

        print(
            f"Request {request_id} : "
            f"{response.status_code}, "
            f"cached = {cached}, "
            f" latency : {elapsed * 1000:.2f} ms " 
        )

        return {
            "request_id": request_id,
            "status_code": response.status_code,
            "cached": cached,
            "latency_ms": elapsed * 1000,
            "error" : False
        }

    except Exception as e:
        elapsed = time.perf_counter() - start_time

        print(
            f"Request {request_id} : "
            f"ERROR, "
            f" latency : {elapsed * 1000:.2f} ms, "
            f"error: {type(e).__name__}: {e}"
        )

        return {
            "request_id": request_id,
            "status_code": None,
            "cached": False,
            "latency_ms": elapsed * 1000,
            "error": True
        }

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:

        tasks = [
            send_request(client, i)
            for i in range(1, NUM_REQUESTS + 1)
        ]

        results = await asyncio.gather(*tasks)

        cache_hits = sum(1 for result in results 
                         if result["cached"])

        cache_hit_rate = (cache_hits/ len(results)) * 100

        successful_results = [
            result for result in results
            if not result["error"] and result ["status_code"] == 200
        ]

        if successful_results:
            average_latency = sum(
                result["latency_ms"]
                for result in successful_results
            )/len(successful_results)

            print(f"average latency : {average_latency:.2f} ms")
            
        print(f"\n Cache hits : {cache_hits}")
        print(f" cache hit rate : {cache_hit_rate: .2f}%")

if __name__ == "__main__":
    asyncio.run(main())
