# demonstrate a Circuit breaker pattern
# requests getting timeout if taking beyond defined time

import asyncio

async def api_request(n):
    await asyncio.sleep(n)
    print(f"Success from API (took {n}s)")

async def fetch_data_from_api(timeout=1.5):
    try:
        # Wrap both requests in one gather call
        # gather() runs them concurrently
        combined_tasks = asyncio.gather(
            api_request(1),
            api_request(2)
        )
        
        # Pass the combined task to wait_for
        await asyncio.wait_for(combined_tasks, timeout=timeout)
        print("Everything finished in time!")
        
    except asyncio.TimeoutError:
        print("Request timed out")

asyncio.run(fetch_data_from_api(1.5))