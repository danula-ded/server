import uuid

from django.utils.deprecation import MiddlewareMixin

from core.logging import correlation_id_var


class CorrelationIdMiddleware(MiddlewareMixin):
    header_name = "HTTP_X_CORRELATION_ID"
    response_header = "X-Correlation-ID"

    def process_request(self, request):
        cid = request.META.get(self.header_name)
        if not cid:
            cid = str(uuid.uuid4())
        request.correlation_id = cid
        correlation_id_var.set(cid)

    def process_response(self, request, response):
        cid = getattr(request, "correlation_id", None)
        if cid:
            response[self.response_header] = cid
        return response
