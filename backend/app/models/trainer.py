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