from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...models.trainer import trainer
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/metrics")
async def get_metrics() -> Dict[str, Dict[str, float]]:
    """Get current model metrics"""
    if not trainer.trained:
        raise HTTPException(status_code=400, detail="Models not trained yet")
    
    return trainer.get_metrics()

@router.get("/compare")
async def compare_models() -> Dict[str, Any]:
    """Get detailed model comparison"""
    if not trainer.trained:
        raise HTTPException(status_code=400, detail="Models not trained yet")
    
    metrics = trainer.get_metrics()
    model_names = trainer.get_model_names()
    
    # Find best model
    best_model = max(metrics.items(), key=lambda x: x[1]['r2'])[0]
    
    # Generate insights
    insights = {
        'best_model': best_model,
        'models_trained': model_names,
        'summary': f"{best_model} performs best with R²={metrics[best_model]['r2']:.3f}",
        'comparison': {}
    }
    
    # Compare each model
    for name in model_names:
        if name != best_model:
            diff = metrics[best_model]['r2'] - metrics[name]['r2']
            insights['comparison'][name] = {
                'difference': round(diff, 4),
                'better': diff < 0
            }
    
    return {
        'metrics': metrics,
        'insights': insights,
        'note': 'Random Forest typically achieves R² ≈ 0.85, XGBoost ≈ 0.87 on housing data'
    }