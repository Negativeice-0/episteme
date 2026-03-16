from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Dict, Any
import numpy as np
from ...models.trainer import trainer
from ...data.datasets import datasets
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class PredictionRequest(BaseModel):
    features: Dict[str, float]
    model: str = "Linear Regression"

class PredictionResponse(BaseModel):
    prediction: float
    model: str
    dataset: str
    units: str
    request_id: str

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: Request, pred_request: PredictionRequest):
    """Make prediction using specified model"""
    
    if not trainer.trained:
        raise HTTPException(status_code=400, detail="Models not trained yet")
    
    try:
        # Get current dataset
        dataset = datasets.get_current_dataset()
        
        # Ensure features are in correct order
        feature_values = []
        missing_features = []
        
        for feature in dataset['features']:
            if feature not in pred_request.features:
                missing_features.append(feature)
            else:
                feature_values.append(pred_request.features[feature])
        
        if missing_features:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing features: {missing_features}"
            )
        
        # Convert to numpy array
        features_array = np.array(feature_values)
        
        # Make prediction
        prediction = trainer.predict(pred_request.model, features_array)
        
        # Log prediction
        logger.info(f"Prediction made using {pred_request.model}: {prediction}")
        
        return PredictionResponse(
            prediction=prediction,
            model=pred_request.model,
            dataset=dataset['name'],
            units=dataset['units'],
            request_id=getattr(request.state, 'request_id', 'unknown')
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed")