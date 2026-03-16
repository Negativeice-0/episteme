# backend/src/utils/logger.py
import logging
import logging.handlers
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import traceback

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent.parent / 'logs'
ERROR_LOG_DIR = LOG_DIR / 'error'
ACCESS_LOG_DIR = LOG_DIR / 'access'
MODEL_LOG_DIR = LOG_DIR / 'model'

for dir_path in [LOG_DIR, ERROR_LOG_DIR, ACCESS_LOG_DIR, MODEL_LOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        if hasattr(record, 'request_id'):
            log_obj['request_id'] = record.request_id
            
        if record.exc_info:
            log_obj['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
            
        if hasattr(record, 'extra_data'):
            log_obj['extra'] = record.extra_data
            
        return json.dumps(log_obj)

def setup_logging(app_name: str = "episteme"):
    """Configure logging for the application"""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Error logger
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG_DIR / f'{app_name}_error.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    
    # Access logger
    access_handler = logging.handlers.RotatingFileHandler(
        ACCESS_LOG_DIR / f'{app_name}_access.log',
        maxBytes=10485760,
        backupCount=5
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(JSONFormatter())
    
    # Model logger
    model_handler = logging.handlers.RotatingFileHandler(
        MODEL_LOG_DIR / f'{app_name}_model.log',
        maxBytes=10485760,
        backupCount=5
    )
    model_handler.setLevel(logging.INFO)
    model_handler.setFormatter(JSONFormatter())
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if os.getenv('ENV') == 'development' else logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    root_logger.addHandler(error_handler)
    root_logger.addHandler(access_handler)
    root_logger.addHandler(model_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

# Create logger instance
logger = setup_logging()

class LoggerMixin:
    """Mixin to add logging capabilities to classes"""
    
    @property
    def logger(self):
        name = '.'.join([self.__class__.__module__, self.__class__.__name__])
        return logging.getLogger(name)