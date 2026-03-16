"""
Episteme Main Application
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .api.routes import (
    health,
    datasets,
    predict,
    metrics,
    socratic
)
from .api.middleware.cors import setup_cors
from .api.middleware.logging import LoggingMiddleware
from .utils.logger import setup_logging
from .core.config import settings
from .data.datasets import datasets as dataset_manager
from .models.trainer import trainer

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENV}")
    
    # Load default dataset and train models
    try:
        dataset = dataset_manager.get_current_dataset()
        logger.info(f"Loading dataset: {dataset['name']}")
        
        # Train initial models
        metrics = trainer.train(dataset['X'], dataset['y'])
        logger.info(f"Models trained successfully: {list(metrics.keys())}")
        
    except Exception as e:
        logger.error(f"Failed to initialize models: {e}", exc_info=True)
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Academic critique engine for machine learning models",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Setup CORS
setup_cors(app)

# Add middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(datasets.router, tags=["Datasets"])
app.include_router(predict.router, tags=["Prediction"])
app.include_router(metrics.router, tags=["Metrics"])
app.include_router(socratic.router, tags=["Learning"])

# Export app for uvicorn
__all__ = ['app']