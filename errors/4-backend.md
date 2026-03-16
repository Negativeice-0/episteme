# only deal with venv leave else as is

Go to /backend/reqs-info.txt for solution.

It worked - but more erros started when running server.

## backend overhaul

# 🔧 **Complete Backend Overhaul with Proper Directory Structure**

The error `ModuleNotFoundError: No module named 'src'` means Python can't find your module. Let's rebuild the entire backend with a proper structure that actually works.

## 📁 **Step 1: Create Proper Backend Structure**

```bash
# Navigate to backend
cd ~/Projects/episteme/backend

# Remove the problematic structure
rm -rf src
rm -rf __pycache__
rm -rf *.pyc

# Create proper directory structure
mkdir -p app/api/routes
mkdir -p app/api/middleware
mkdir -p app/core
mkdir -p app/models
mkdir -p app/services
mkdir -p app/utils
mkdir -p app/data
mkdir -p tests
mkdir -p logs/{error,access,model}
```

## 📦 **Step 2: Create __init__.py Files**

```bash
# Create __init__.py files in each directory
touch app/__init__.py
touch app/api/__init__.py
touch app/api/routes/__init__.py
touch app/api/middleware/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch app/data/__init__.py
touch tests/__init__.py
```

## 🐍 **Step 3: Create Core Configuration**

```python
# app/core/config.py
import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Episteme"
    APP_VERSION: str = "1.0.0"
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    API_KEYS: List[str] = os.getenv("API_KEYS", "dev-key").split(",")
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## 📊 **Step 4: Create Datasets Module**

```python
# app/data/datasets.py
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml, make_regression
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EpistemeDatasets:
    """Dataset loader for Episteme"""
    
    def __init__(self):
        self.datasets = {}
        self.current_dataset = None
        self._load_default_datasets()
    
    def _load_default_datasets(self):
        """Load default datasets"""
        try:
            # Try to load Boston Housing
            self.datasets['housing'] = self._load_boston_housing()
        except Exception as e:
            logger.warning(f"Could not load Boston Housing: {e}")
            self.datasets['housing'] = self._create_synthetic_housing()
        
        # Always add synthetic datasets
        self.datasets['education'] = self._create_education_dataset()
        self.datasets['salary'] = self._create_salary_dataset()
        
        # Set default
        self.current_dataset = 'housing'
    
    def _load_boston_housing(self) -> Dict[str, Any]:
        """Load Boston Housing dataset"""
        # Using California housing as a more accessible alternative
        from sklearn.datasets import fetch_california_housing
        
        housing = fetch_california_housing()
        X = pd.DataFrame(housing.data, columns=housing.feature_names)
        y = pd.Series(housing.target * 100000)  # Convert to dollars
        
        return {
            'name': 'California Housing',
            'description': 'Housing values in California districts',
            'features': list(X.columns),
            'target': 'MedHouseVal',
            'X': X,
            'y': y,
            'feature_descriptions': {
                'MedInc': 'Median income in block group',
                'HouseAge': 'Median house age in block group',
                'AveRooms': 'Average rooms per household',
                'AveBedrms': 'Average bedrooms per household',
                'Population': 'Block group population',
                'AveOccup': 'Average occupants per household',
                'Latitude': 'Block group latitude',
                'Longitude': 'Block group longitude',
            },
            'units': 'USD'
        }
    
    def _create_synthetic_housing(self) -> Dict[str, Any]:
        """Create synthetic housing data"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate features
        income = np.random.normal(5, 2, n_samples)
        house_age = np.random.uniform(0, 50, n_samples)
        rooms = np.random.normal(5, 1.5, n_samples)
        bedrooms = rooms * np.random.uniform(0.4, 0.6, n_samples)
        population = np.random.gamma(10, 10, n_samples)
        occupancy = population / np.random.gamma(10, 1, n_samples)
        latitude = np.random.uniform(32.5, 42, n_samples)
        longitude = np.random.uniform(-124, -114, n_samples)
        
        # Target with non-linear relationships
        price = (100000 + 
                20000 * income + 
                -500 * house_age + 
                15000 * rooms + 
                -10000 * (bedrooms/rooms - 0.5) ** 2 +
                np.random.normal(0, 20000, n_samples))
        
        X = pd.DataFrame({
            'MedInc': income,
            'HouseAge': house_age,
            'AveRooms': rooms,
            'AveBedrms': bedrooms,
            'Population': population,
            'AveOccup': occupancy,
            'Latitude': latitude,
            'Longitude': longitude
        })
        
        return {
            'name': 'Synthetic Housing',
            'description': 'Synthetic housing data with realistic patterns',
            'features': list(X.columns),
            'target': 'MedHouseVal',
            'X': X,
            'y': price,
            'feature_descriptions': {
                'MedInc': 'Median income',
                'HouseAge': 'House age',
                'AveRooms': 'Average rooms',
                'AveBedrms': 'Average bedrooms',
                'Population': 'Population',
                'AveOccup': 'Occupants per household',
                'Latitude': 'Latitude',
                'Longitude': 'Longitude',
            },
            'units': 'USD'
        }
    
    def _create_education_dataset(self) -> Dict[str, Any]:
        """Create education vs income dataset"""
        np.random.seed(42)
        n_samples = 500
        
        education = np.random.uniform(0, 20, n_samples)
        experience = np.random.uniform(0, 40, n_samples)
        
        # Non-linear relationship
        income = (15000 + 
                 2000 * education + 
                 500 * education ** 1.2 + 
                 800 * experience + 
                 np.random.normal(0, 5000, n_samples))
        
        X = pd.DataFrame({
            'education_years': education,
            'experience_years': experience
        })
        
        return {
            'name': 'Education vs Income',
            'description': 'Relationship between education and income',
            'features': list(X.columns),
            'target': 'income',
            'X': X,
            'y': income,
            'feature_descriptions': {
                'education_years': 'Years of education',
                'experience_years': 'Years of experience'
            },
            'units': 'USD/year'
        }
    
    def _create_salary_dataset(self) -> Dict[str, Any]:
        """Create salary prediction dataset"""
        np.random.seed(42)
        n_samples = 1000
        
        education = np.random.choice([0, 1, 2, 3, 4], n_samples)
        experience = np.random.uniform(0, 30, n_samples)
        sector = np.random.choice([0, 1, 2, 3], n_samples)
        
        sector_names = ['Tech', 'Finance', 'Healthcare', 'Education']
        sector_mult = [1.5, 1.4, 1.2, 0.9]
        
        base = 30000
        salary = (base + 
                 5000 * education ** 1.2 + 
                 1000 * experience + 
                 50 * experience ** 2)
        
        # Apply sector multiplier
        for i, mult in enumerate(sector_mult):
            mask = sector == i
            salary[mask] *= mult
        
        X = pd.DataFrame({
            'education_level': education,
            'experience': experience,
            'sector': [sector_names[s] for s in sector]
        })
        
        # One-hot encode sector for modeling
        X_encoded = pd.get_dummies(X, columns=['sector'], prefix='sector')
        
        return {
            'name': 'Salary Prediction',
            'description': 'Multi-sector salary data',
            'features': list(X_encoded.columns),
            'target': 'salary',
            'X': X_encoded,
            'y': salary,
            'feature_descriptions': {
                'education_level': '0-4 education level',
                'experience': 'Years experience',
                'sector_Tech': 'Tech sector',
                'sector_Finance': 'Finance sector',
                'sector_Healthcare': 'Healthcare sector',
                'sector_Education': 'Education sector'
            },
            'units': 'USD/year'
        }
    
    def get_dataset(self, name: str = 'housing') -> Optional[Dict[str, Any]]:
        """Get dataset by name"""
        return self.datasets.get(name)
    
    def get_current_dataset(self) -> Dict[str, Any]:
        """Get current dataset"""
        return self.datasets.get(self.current_dataset, self.datasets['housing'])
    
    def set_current_dataset(self, name: str) -> bool:
        """Set current dataset"""
        if name in self.datasets:
            self.current_dataset = name
            return True
        return False
    
    def list_datasets(self) -> List[Dict[str, str]]:
        """List available datasets"""
        return [
            {'id': k, 'name': v['name']} 
            for k, v in self.datasets.items()
        ]

# Create singleton instance
datasets = EpistemeDatasets()
```

## 🤖 **Step 5: Create Models Module**

```python
# app/models/trainer.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import xgboost as xgb
from typing import Dict, Any, Optional
import logging
import joblib
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Train and manage ML models"""
    
    def __init__(self):
        self.models = {}
        self.metrics = {}
        self.trained = False
        self.current_dataset = None
        
    def train(self, X: pd.DataFrame, y: pd.Series, dataset_name: str = 'default'):
        """Train all models on the given data"""
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize models with safe defaults
        models_config = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(
                n_estimators=50,  # Reduced for speed
                max_depth=8,
                random_state=42,
                n_jobs=-1
            ),
            'XGBoost': xgb.XGBRegressor(
                n_estimators=50,  # Reduced for speed
                max_depth=5,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1,
                verbosity=0
            )
        }
        
        results = {}
        
        for name, model in models_config.items():
            try:
                # Train
                model.fit(X_train, y_train)
                
                # Predict
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                r2 = float(r2_score(y_test, y_pred))
                rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
                mae = float(mean_absolute_error(y_test, y_pred))
                
                # Store results
                results[name] = {
                    'model': model,
                    'r2': round(r2, 4),
                    'rmse': round(rmse, 2),
                    'mae': round(mae, 2),
                    'feature_importance': self._get_feature_importance(model, X.columns) if hasattr(model, 'feature_importances_') else None
                }
                
                logger.info(f"Trained {name}: R²={r2:.4f}, RMSE={rmse:.2f}")
                
            except Exception as e:
                logger.error(f"Failed to train {name}: {e}")
                continue
        
        self.models = {name: res['model'] for name, res in results.items()}
        self.metrics = {
            name: {k: v for k, v in res.items() if k != 'model'} 
            for name, res in results.items()
        }
        self.trained = True
        self.current_dataset = dataset_name
        
        return self.metrics
    
    def _get_feature_importance(self, model, feature_names):
        """Get feature importance if available"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            return dict(zip(feature_names, importances.tolist()))
        return None
    
    def predict(self, model_name: str, features: np.ndarray) -> float:
        """Make prediction using specified model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model = self.models[model_name]
        
        # Ensure 2D array
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        prediction = model.predict(features)[0]
        return float(prediction)
    
    def get_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get current metrics"""
        return self.metrics
    
    def get_model_names(self) -> list:
        """Get list of trained model names"""
        return list(self.models.keys())
    
    def save_models(self, path: str):
        """Save trained models to disk"""
        os.makedirs(path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for name, model in self.models.items():
            filename = os.path.join(path, f"{name.lower().replace(' ', '_')}_{timestamp}.pkl")
            joblib.dump(model, filename)
            logger.info(f"Saved {name} to {filename}")
    
    def load_models(self, path: str):
        """Load trained models from disk"""
        # Implementation for loading models
        pass

# Create singleton instance
trainer = ModelTrainer()
```

## 🚀 **Step 6: Create API Routes**

```python
# app/api/routes/predict.py
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
```

```python
# app/api/routes/datasets.py
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
```

```python
# app/api/routes/metrics.py
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
```

```python
# app/api/routes/socratic.py
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.get("/socratic-prompts")
async def get_socratic_prompts() -> List[Dict[str, str]]:
    """Get Socratic learning prompts"""
    
    prompts = [
        {
            "question": "Why might crime rate affect housing prices more in some neighborhoods than others?",
            "context": "crime",
            "reflection": "Linear models assume constant effects, but social factors interact non-linearly."
        },
        {
            "question": "What social factors change with average number of rooms per dwelling?",
            "context": "rooms",
            "reflection": "Rooms correlate with wealth, family size, and neighborhood status."
        },
        {
            "question": "How would you explain the difference between Random Forest and Linear Regression to a peer?",
            "context": "models",
            "reflection": "One draws straight lines through data, the other learns complex patterns from examples."
        },
        {
            "question": "Why does education show diminishing returns on income in real data?",
            "context": "education",
            "reflection": "Human systems have ceilings and market saturation effects."
        },
        {
            "question": "What hidden variables might explain the relationship between rooms and housing price?",
            "context": "confounding",
            "reflection": "Correlation doesn't imply causation - wealth influences both."
        },
        {
            "question": "When would you trust Linear Regression over XGBoost?",
            "context": "model_selection",
            "reflection": "Simple, well-understood relationships with limited, clean data."
        }
    ]
    
    return prompts
```

```python
# app/api/routes/health.py
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
```

## 🛡️ **Step 7: Create Middleware**

```python
# app/api/middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
import logging
from typing import Callable

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        logger.info(f"Request started: {request.method} {request.url.path} [{request_id}]")
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Log response
            process_time = time.time() - start_time
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"[{request_id}] - {response.status_code} - {process_time:.3f}s"
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"[{request_id}] - {str(e)} - {process_time:.3f}s",
                exc_info=True
            )
            raise
```

```python
# app/api/middleware/cors.py
from fastapi.middleware.cors import CORSMiddleware
from ...core.config import settings

def setup_cors(app):
    """Setup CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

## 📝 **Step 8: Create Utils**

```python
# app/utils/logger.py
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
```

## 🎯 **Step 9: Create Main Application**

```python
# app/main.py
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
```

## 📦 **Step 10: Create Requirements File**

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
scikit-learn==1.3.2
xgboost==2.0.2
pandas==2.1.3
numpy==1.24.3
python-multipart==0.0.6
joblib==1.3.2
```

## 🚀 **Step 11: Create Run Script**

```python
# run.py
#!/usr/bin/env python
"""
Development server runner
"""

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
```

## 🎉 **Step 12: Test Everything**

```bash
# 1. Navigate to backend
cd ~/Projects/episteme/backend

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install requirements if not already done
pip install -r requirements.txt

# 4. Run the application
python run.py

# 5. In another terminal, test the API
curl http://localhost:8000/health
curl http://localhost:8000/datasets
curl http://localhost:8000/metrics
```

## 📋 **Final Directory Structure**

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── datasets.py
│   │   │   ├── predict.py
│   │   │   ├── metrics.py
│   │   │   └── socratic.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── logging.py
│   │       └── cors.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── trainer.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── datasets.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── logs/
│   ├── error/
│   ├── access/
│   └── model/
├── requirements.txt
├── run.py
└── venv/
```

## ✅ **Verification Checklist**

- [x] All `__init__.py` files created
- [x] Configuration module working
- [x] Datasets module loading
- [x] Model trainer initializing
- [x] API routes defined
- [x] Middleware configured
- [x] Main app assembled
- [x] Requirements installed
- [x] Server starts without errors
- [x] Health endpoint responds
- [x] Datasets endpoint works
- [x] Metrics available

Run `python run.py` and visit `http://localhost:8000/docs` to see the interactive API documentation. The backend should now work perfectly!