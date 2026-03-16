from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ...data.datasets import datasets
from ...models.trainer import trainer
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/datasets")
async def list_datasets() -> List[Dict[str, str]]:
    """List available datasets"""
    return datasets.list_datasets()

@router.get("/dataset/{dataset_id}")
async def get_dataset_info(dataset_id: str) -> Dict[str, Any]:
    """Get detailed information about a dataset"""
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Return metadata only (not the full data)
    return {
        'id': dataset_id,
        'name': dataset['name'],
        'description': dataset['description'],
        'features': dataset['features'],
        'target': dataset['target'],
        'feature_descriptions': dataset['feature_descriptions'],
        'units': dataset['units'],
        'n_samples': len(dataset['X']),
        'n_features': len(dataset['features'])
    }

@router.post("/switch-dataset/{dataset_id}")
async def switch_dataset(dataset_id: str) -> Dict[str, Any]:
    """Switch to a different dataset and retrain models"""
    
    if not datasets.set_current_dataset(dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        # Get current dataset
        dataset = datasets.get_current_dataset()
        
        # Retrain models
        metrics = trainer.train(dataset['X'], dataset['y'], dataset_id)
        
        logger.info(f"Switched to dataset: {dataset['name']}")
        
        return {
            "message": f"Switched to {dataset['name']} dataset",
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Failed to switch dataset: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to switch dataset")