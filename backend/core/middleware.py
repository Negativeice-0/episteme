import logging
import uuid
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Simple request logging middleware"""
    
    def process_request(self, request):
        request.request_id = str(uuid.uuid4())
        
    def process_response(self, request, response):
        response['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
        return response
