import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class JSONFormatter:
    """Format data as JSON for logging"""
    
    @staticmethod
    def format(data):
        try:
            return json.dumps(data, indent=2, default=str)
        except:
            return str(data)

def log_model_training(model_name, metrics, dataset_name):
    """Log model training metrics"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'model': model_name,
        'metrics': metrics,
        'dataset': dataset_name,
    }
    logger.info(f"Model training: {JSONFormatter.format(log_entry)}")
