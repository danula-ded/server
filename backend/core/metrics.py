from collections.abc import Callable
from functools import wraps

from django.http import HttpResponse
from prometheus_client import Histogram
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

INTEGRATION_LATENCY_SECONDS = Histogram(
    "integration_latency_seconds",
    "Latency of integration calls in seconds",
    labelnames=("operation",),
)


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


def track_latency(operation: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with INTEGRATION_LATENCY_SECONDS.labels(operation=operation).time():
                return func(*args, **kwargs)

        return wrapper

    return decorator
