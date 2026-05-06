import asyncio

import logging
from app.metrics.context import get_trace_id

logger = logging.getLogger(__name__)
async def monitor_event_loop(interval: float = 1.0):
    loop = asyncio.get_event_loop()

    while True:
        start = loop.time()

        await asyncio.sleep(interval)

        lag = (loop.time() - start - interval) * 1000

        logger.debug({
            'trace_id': get_trace_id(),
            'metric': 'event_loop_lag_ms',
            'value': round(lag, 3)
        })