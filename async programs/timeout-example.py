# demonstrate a Circuit breaker pattern
# requests getting timeout if taking beyond defined time

import asyncio

async def api_request(n):
    await asyncio.sleep(n)
    print(f"Success from API (took {n}s)")

########### Example 1 - using asyncio.wait_for()
async def fetch_data_using_wait_for(timeout=1.5):
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

print("---------- Example 1 -------------")
asyncio.run(fetch_data_using_wait_for(1.5))



######### Example 2 - Using asyncio.wait()
async def fetch_data_using_wait(timeout=1.5):
    try:
         # 1. Wrap your calls in Tasks so they start running
        task1 = asyncio.create_task(api_request(1))
        task2 = asyncio.create_task(api_request(2))
        
        # 2. Use asyncio.wait with a timeout
        done, pending = await asyncio.wait([task1, task2], timeout=timeout)
        
        print(f"Finished tasks: {len(done)}")
        for task in done:
            print(f"Result: {task.result()}")
            
        print(f"Timed out tasks: {len(pending)}")
        for task in pending:
            # 3. Clean up: Cancel tasks that didn't finish
            task.cancel()
        
    except asyncio.TimeoutError:
        print("Request timed out")

print("---------- Example 2 -------------")
asyncio.run(fetch_data_using_wait(1.5))