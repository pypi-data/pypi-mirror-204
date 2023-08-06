from __future__ import annotations

import asyncio
from typing import Callable, Iterable, Set

from aiolimiter import AsyncLimiter


def concunrrently_handle_tasks(
    task_fns: Iterable, max_rate: float = 20, time_period: float = 6
) -> Set[asyncio.Task]:
    """
    Creates and runs asynchronous tasks concurrently with a maximum rate of execution using an AsyncLimiter.

    Args:
        task_fns (Iterable): An iterable of callable objects to execute asynchronously.
        max_rate (float, optional): The maximum rate of execution in tasks per second. Defaults to 20.
        time_period (float, optional): The length of the time period used to calculate the rate in seconds. Defaults to 6.

    Returns:
        Set[asyncio.Task]: A set of asyncio tasks that were created and executed.
    """
    limiter = AsyncLimiter(max_rate, time_period)

    async def _wrapper(task_fn: Callable, limiter: AsyncLimiter):
        async with limiter:
            return task_fn()

    async def _handler(tasks):
        tasks = [_wrapper(task_fn, limiter) for task_fn in tasks]
        return await asyncio.wait(tasks)

    results, _ = asyncio.run(_handler(task_fns))
    return results


def sanitize_description(description: str) -> str:
    """Sanitize a description to a Shopify description."""
    # Replace /n with <br>
    description = description.replace("/n", "<br>")
    # Replace /t with &nbsp;
    description = description.replace("/t", "&nbsp;")
    return description