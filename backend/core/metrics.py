from collections.abc import Callable
from functools import wraps

from prometheus_client import Histogram

INTEGRATION_LATENCY_SECONDS = Histogram(
    "integration_latency_seconds",
    "Latency of integration calls in seconds",
    labelnames=("operation",),
)


def track_latency(operation: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with INTEGRATION_LATENCY_SECONDS.labels(operation=operation).time():
                return func(*args, **kwargs)

        return wrapper

    return decorator
