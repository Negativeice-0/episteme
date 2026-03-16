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