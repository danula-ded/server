from prometheus_client import Counter

REQUESTS_TOTAL = Counter("http_requests_total", "Total HTTP requests")
RESPONSES_2XX_TOTAL = Counter("http_responses_2xx_total", "Total 2xx responses")
RESPONSES_4XX_TOTAL = Counter("http_responses_4xx_total", "Total 4xx responses")
RESPONSES_5XX_TOTAL = Counter("http_responses_5xx_total", "Total 5xx responses")


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        REQUESTS_TOTAL.inc()
        response = self.get_response(request)

        status = getattr(response, "status_code", 0)
        if 200 <= status <= 299:
            RESPONSES_2XX_TOTAL.inc()
        elif 400 <= status <= 499:
            RESPONSES_4XX_TOTAL.inc()
        elif 500 <= status <= 599:
            RESPONSES_5XX_TOTAL.inc()

        return response
