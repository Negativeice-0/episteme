import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..core.config import settings

def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory
    log_dir = Path(settings.LOGS_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handlers
    handlers = {
        'error': RotatingFileHandler(
            log_dir / 'error/error.log',
            maxBytes=10485760,
            backupCount=5
        ),
        'access': RotatingFileHandler(
            log_dir / 'access/access.log',
            maxBytes=10485760,
            backupCount=5
        ),
        'model': RotatingFileHandler(
            log_dir / 'model/model.log',
            maxBytes=10485760,
            backupCount=5
        )
    }
    
    for name, handler in handlers.items():
        handler.setFormatter(formatter)
        if name == 'error':
            handler.setLevel(logging.ERROR)
        else:
            handler.setLevel(logging.INFO)
        root_logger.addHandler(handler)
    
    return root_logger