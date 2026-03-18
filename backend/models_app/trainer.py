import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib
import os
from django.conf import settings

from .models import TrainedModel
from datasets.models import Dataset

class ModelTrainer:
    """Train and evaluate ML models"""
    
    def __init__(self):
        self.models = {}
        self.metrics = {}
    
    def train_on_dataset(self, dataset_id):
        """Train all models on a specific dataset"""
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            dataset = Dataset.objects.get(name=dataset_id)  # Try name
        
        # Convert to DataFrame
        df = pd.DataFrame(dataset.data)
        X = df[dataset.features]
        y = df[dataset.target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Models to train
        models_config = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(
                n_estimators=50, max_depth=8, random_state=42, n_jobs=-1
            ),
            'XGBoost': xgb.XGBRegressor(
                n_estimators=50, max_depth=5, learning_rate=0.1,
                random_state=42, n_jobs=-1, verbosity=0
            )
        }
        
        results = {}
        
        for name, model in models_config.items():
            print(f"  Training {name}...")
            
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            r2 = float(r2_score(y_test, y_pred))
            rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
            mae = float(mean_absolute_error(y_test, y_pred))
            
            # Save model
            model_type = name.lower().replace(' ', '_')
            filename = f"{model_type}_{dataset.id}.pkl"
            filepath = os.path.join(settings.BASE_DIR, 'saved_models', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            joblib.dump(model, filepath)
            
            # Save to database
            trained, created = TrainedModel.objects.update_or_create(
                name=model_type[:3],  # 'lr', 'rf', 'xgb'
                dataset=dataset,
                defaults={
                    'metrics': {'r2': r2, 'rmse': rmse, 'mae': mae},
                    'feature_importance': self._get_feature_importance(model, X.columns),
                    'file_path': filepath,
                    'is_active': True
                }
            )
            
            results[name] = {
                'r2': round(r2, 4),
                'rmse': round(rmse, 2),
                'mae': round(mae, 2)
            }
            
            print(f"    ✓ R²={r2:.4f}, RMSE={rmse:.2f}")
        
        return results
    
    def _get_feature_importance(self, model, feature_names):
        """Get feature importance if available"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            return dict(zip(feature_names, importances.tolist()))
        return {}
    
    def predict(self, model_name, dataset_id, features):
        """Make prediction using trained model"""
        try:
            trained = TrainedModel.objects.get(
                name=model_name,
                dataset_id=dataset_id,
                is_active=True
            )
            model = joblib.load(trained.file_path)
            
            # Convert features to array
            if isinstance(features, dict):
                features = np.array([list(features.values())])
            elif isinstance(features, list):
                features = np.array([features])
            
            prediction = model.predict(features)[0]
            return float(prediction)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

# Create singleton
trainer = ModelTrainer()