from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses"""
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'error': True,
            'code': response.status_code,
            'message': str(exc),
            'type': exc.__class__.__name__,
        }
    else:
        response = Response({
            'error': True,
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal server error',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
