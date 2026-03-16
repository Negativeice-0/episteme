from fastapi import APIRouter
from datetime import datetime
from ...models.trainer import trainer
from ...data.datasets import datasets

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "models_trained": trainer.trained,
        "current_dataset": datasets.current_dataset,
        "available_models": trainer.get_model_names() if trainer.trained else []
    }

@router.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "name": "Episteme API",
        "version": "1.0.0",
        "mission": "AI frees students to reflect, not aggregate.",
        "status": "operational",
        "docs": "/docs"
    }