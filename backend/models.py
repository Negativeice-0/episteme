"""
Episteme - Model training and evaluation module
Trains and compares Linear Regression, Random Forest, and XGBoost models
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import xgboost as xgb
import json

class EpistemeModels:
    """Model training and comparison for Episteme's critique engine"""
    
    def __init__(self):
        self.models = {}
        self.metrics = {}
        self.trained = False
    
    def train_and_evaluate(self, X, y, dataset_name='default'):
        """
        Train all models and compute evaluation metrics
        
        Args:
            X: Feature matrix
            y: Target vector
            dataset_name: Name of the dataset for reference
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(
                n_estimators=100, 
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'XGBoost': xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
        }
        
        results = {}
        
        for name, model in models.items():
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            
            # Store results
            results[name] = {
                'model': model,
                'r2': round(r2, 4),
                'rmse': round(rmse, 2),
                'mae': round(mae, 2),
                'predictions': y_pred.tolist()[:10],  # First 10 predictions
                'actual': y_test.tolist()[:10]
            }
        
        self.models = {name: res['model'] for name, res in results.items()}
        self.metrics = {
            name: {k: v for k, v in res.items() if k != 'model'} 
            for name, res in results.items()
        }
        self.trained = True
        self.dataset_name = dataset_name
        
        return self.metrics
    
    def predict(self, model_name, features):
        """Make prediction using specified model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model = self.models[model_name]
        
        # Convert features to numpy array if it's a list
        if isinstance(features, list):
            features = np.array(features).reshape(1, -1)
        elif isinstance(features, dict):
            features = np.array(list(features.values())).reshape(1, -1)
        
        prediction = model.predict(features)[0]
        return round(prediction, 2)
    
    def get_comparison_insights(self):
        """Generate insights about model performance"""
        if not self.trained:
            return {}
        
        insights = {}
        
        # Compare Linear Regression vs RF
        lr_r2 = self.metrics['Linear Regression']['r2']
        rf_r2 = self.metrics['Random Forest']['r2']
        xgb_r2 = self.metrics['XGBoost']['r2']
        
        insights['best_model'] = max(
            self.metrics.items(), 
            key=lambda x: x[1]['r2']
        )[0]
        
        insights['linear_limitations'] = (
            f"Linear Regression (R²={lr_r2:.3f}) underperforms "
            f"Random Forest (R²={rf_r2:.3f}) by {((rf_r2 - lr_r2)/lr_r2*100):.1f}%"
            if rf_r2 > lr_r2 else "Linear Regression performs competitively"
        )
        
        insights['xgboost_edge'] = (
            f"XGBoost achieves {xgb_r2:.3f} R², capturing non-linear patterns "
            f"that linear models miss"
        )
        
        # Add educational commentary
        insights['educational_commentary'] = {
            'linear': (
                "Linear Regression assumes independent, linear relationships. "
                "In human systems, factors interact non-linearly."
            ),
            'rf': (
                "Random Forest captures interactions and non-linearities "
                "through ensemble decision trees."
            ),
            'xgb': (
                "XGBoost's gradient boosting often outperforms by iteratively "
                "correcting previous errors."
            )
        }
        
        return insights
    
    def get_benchmark_notes(self):
        """Get standardized benchmark notes for UI"""
        return {
            'Linear Regression': {
                'typical_r2': '0.65 - 0.75',
                'typical_rmse': '4.5 - 5.5',
                'note': 'Assumes linear relationships - often oversimplifies'
            },
            'Random Forest': {
                'typical_r2': '0.82 - 0.88',
                'typical_rmse': '3.2 - 3.8',
                'note': 'Captures non-linear patterns well'
            },
            'XGBoost': {
                'typical_r2': '0.85 - 0.90',
                'typical_rmse': '2.9 - 3.5',
                'note': 'State-of-the-art for tabular data'
            }
        }