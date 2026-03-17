from django.http import JsonResponse
from datetime import datetime

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'message': 'Episteme API is running'
    })
