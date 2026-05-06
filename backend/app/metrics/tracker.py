import time
import inspect
from functools import wraps

import logging
from app.metrics.context import get_trace_id

logger = logging.getLogger(__name__)
def log_metric(metric_name: str, value: float):
    logger.info({
        'trace_id': get_trace_id(),
        'metric': metric_name,
        'value_ms': round(value, 3)
    })

def track(metric_name: str):
    def decorator(func):

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = await func(*args, **kwargs)

                duration = (time.perf_counter() - start) * 1000
                log_metric(metric_name, duration)
                return result
            
            return async_wrapper
        
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()

                result = func(*args, **kwargs)

                duration = (time.perf_counter() - start) * 1000
                log_metric(metric_name, duration)

                return result
            return sync_wrapper
    return decorator