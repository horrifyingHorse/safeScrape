import asyncio
import random


async def human_like_delay(min_time: float = 0.5, max_time: float = 3.5):
    """Simulate human-like random delays."""
    await asyncio.sleep(random.uniform(min_time, max_time))
