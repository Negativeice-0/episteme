# backend/src/api/middleware/error_tracking.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import uuid
from typing import Callable
from ...utils.logger import logger
import functools

async def error_tracking_middleware(request: Request, call_next: Callable):
    """Middleware to track errors and request performance"""
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add request ID to logger
    old_factory = logging.getLogRecordFactory()
    
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = request_id
        return record
    
    logging.setLogRecordFactory(record_factory)
    
    # Track request timing
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Log successful request
        process_time = time.time() - start_time
        logger.info(
            f"Request completed",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'status_code': response.status_code,
                'process_time': process_time
            }
        )
        
        response.headers['X-Request-ID'] = request_id
        return response
        
    except Exception as e:
        # Log error
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {str(e)}",
            exc_info=True,
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'process_time': process_time,
                'error_type': type(e).__name__
            }
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={
                'error': 'Internal server error',
                'request_id': request_id,
                'message': str(e) if os.getenv('ENV') == 'development' else 'An error occurred'
            }
        )