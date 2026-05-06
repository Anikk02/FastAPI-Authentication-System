import psutil
import asyncio

import logging
from app.metrics.context import get_trace_id

logger = logging.getLogger(__name__)

async def monitor_system(interval: int = 5):
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent

        logger.info({
            'trace_id': get_trace_id(),
            'metric': 'cpu_usage_percent',
            'value': cpu
        })

        logger.info({
            'trace_id': get_trace_id(),
            'metric': 'memory_usage_percent',
            'value': memory
        })

        await asyncio.sleep(interval)