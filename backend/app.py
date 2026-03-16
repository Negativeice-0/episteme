"""
Episteme - Main FastAPI Application
Academic critique engine for Linear Regression vs Modern ML models
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

from data.datasets import EpistemeDatasets
from models import EpistemeModels

# Initialize FastAPI
app = FastAPI(
    title="Episteme - Academic Critique Engine",
    description="AI for reflection, not drudgery. Compare Linear Regression vs Random Forest vs XGBoost.",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://episteme.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize datasets and models
datasets = EpistemeDatasets()
models = EpistemeModels()

# Load default dataset (housing) and train models
default_dataset = datasets.get_dataset('housing')
if default_dataset:
    models.train_and_evaluate(
        default_dataset['X'], 
        default_dataset['y'],
        dataset_name='housing'
    )

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    features: Dict[str, float]
    model: str = "Linear Regression"

class PredictionResponse(BaseModel):
    prediction: float
    model: str
    dataset: str
    units: str

class ComparisonResponse(BaseModel):
    metrics: Dict[str, Dict[str, float]]
    insights: Dict
    benchmark_notes: Dict

class DatasetInfo(BaseModel):
    id: str
    name: str
    description: str
    features: List[str]
    target: str
    feature_descriptions: Dict[str, str]
    units: str

# API Endpoints

@app.get("/")
async def root():
    """Welcome endpoint with mission statement"""
    return {
        "name": "Episteme",
        "mission": "AI frees students to reflect, not aggregate.",
        "version": "1.0.0",
        "message": "Welcome to the academic critique engine for machine learning models."
    }

@app.get("/datasets", response_model=List[Dict])
async def get_datasets():
    """Get list of available datasets"""
    return datasets.get_dataset_list()

@app.get("/dataset/{dataset_id}", response_model=DatasetInfo)
async def get_dataset_info(dataset_id: str):
    """Get detailed information about a specific dataset"""
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return DatasetInfo(
        id=dataset_id,
        name=dataset['name'],
        description=dataset['description'],
        features=dataset['features'],
        target=dataset['target'],
        feature_descriptions=dataset['feature_descriptions'],
        units=dataset['units']
    )

@app.post("/switch-dataset/{dataset_id}")
async def switch_dataset(dataset_id: str):
    """Switch to a different dataset and retrain models"""
    dataset = datasets.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    global models
    models = EpistemeModels()
    metrics = models.train_and_evaluate(
        dataset['X'], 
        dataset['y'],
        dataset_name=dataset_id
    )
    
    return {
        "message": f"Switched to {dataset['name']} dataset",
        "metrics": metrics
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make prediction using specified model"""
    if not models.trained:
        raise HTTPException(status_code=400, detail="Models not trained yet")
    
    try:
        # Get current dataset for feature ordering
        current_dataset = datasets.get_dataset(models.dataset_name)
        
        # Ensure features are in correct order
        feature_values = []
        for feature in current_dataset['features']:
            if feature not in request.features:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing feature: {feature}"
                )
            feature_values.append(request.features[feature])
        
        prediction = models.predict(request.model, feature_values)
        
        return PredictionResponse(
            prediction=prediction,
            model=request.model,
            dataset=current_dataset['name'],
            units=current_dataset['units']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/compare", response_model=ComparisonResponse)
async def compare():
    """Get comparison metrics for all models"""
    if not models.trained:
        raise HTTPException(status_code=400, detail="Models not trained yet")
    
    return ComparisonResponse(
        metrics=models.metrics,
        insights=models.get_comparison_insights(),
        benchmark_notes=models.get_benchmark_notes()
    )

@app.get("/metrics")
async def get_metrics():
    """Get R², RMSE, MAE for all models"""
    if not models.trained:
        raise HTTPException(status_code=400, detail="Models not trained yet")
    
    return models.metrics

@app.get("/socratic-prompts")
async def get_socratic_prompts():
    """Get Socratic learning prompts for reflection"""
    prompts = [
        {
            "question": "Why might crime rate affect housing prices more in some neighborhoods than others?",
            "context": "crime_rate",
            "reflection": "Linear models assume constant effects, but social factors interact."
        },
        {
            "question": "What social factors change with average number of rooms per dwelling?",
            "context": "rooms",
            "reflection": "Rooms correlate with wealth, family size, and neighborhood status."
        },
        {
            "question": "How would you explain the difference between Random Forest and Linear Regression to a peer?",
            "context": "model_comparison",
            "reflection": "One draws straight lines, the other learns complex patterns from data."
        },
        {
            "question": "Why does education show diminishing returns on income in real data?",
            "context": "education",
            "reflection": "Human systems have ceilings and market saturation."
        },
        {
            "question": "What hidden variables might explain the relationship between rooms and housing price?",
            "context": "confounding",
            "reflection": "Correlation doesn't imply causation - wealth influences both."
        },
        {
            "question": "When would you trust Linear Regression over XGBoost?",
            "context": "model_selection",
            "reflection": "Simple, well-understood relationships with limited data."
        }
    ]
    return prompts

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_trained": models.trained,
        "current_dataset": getattr(models, 'dataset_name', 'none')
    }

# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)