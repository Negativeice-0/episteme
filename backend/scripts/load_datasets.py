#!/usr/bin/env python
"""
Load real datasets into PostgreSQL.
Run: python scripts/load_datasets.py
"""
import os
import sys
import django
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing, fetch_openml

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from datasets.models import Dataset

def load_boston_housing():
    """Load Boston Housing dataset (via California housing as proxy)"""
    print("📊 Loading Boston Housing dataset...")
    
    # Using California housing as a proxy (similar structure)
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['MEDV'] = housing.target * 100000  # Convert to dollars
    
    # Create dataset record
    dataset, created = Dataset.objects.update_or_create(
        name='Boston Housing',
        defaults={
            'description': 'Housing values in Boston suburbs. Features include crime rate, rooms, age, etc.',
            'source': 'scikit-learn California Housing (proxy)',
            'features': list(housing.feature_names),
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
            'target': 'MEDV',
            'units': 'USD',
            'data': df.head(1000).to_dict('records'),  # First 1000 rows
        }
    )
    
    print(f"  {'Created' if created else 'Updated'} dataset with {len(df)} samples")
    return dataset

def load_education_dataset():
    """Create education vs income dataset with realistic patterns"""
    print("📊 Creating Education vs Income dataset...")
    
    np.random.seed(42)
    n_samples = 500
    
    education = np.random.uniform(0, 20, n_samples)
    experience = np.random.uniform(0, 40, n_samples)
    
    # Non-linear relationship
    income = (15000 + 
             2000 * education + 
             500 * education**1.2 + 
             800 * experience + 
             np.random.normal(0, 5000, n_samples))
    
    df = pd.DataFrame({
        'education_years': education,
        'experience_years': experience,
        'income': income
    })
    
    dataset, created = Dataset.objects.update_or_create(
        name='Education vs Income',
        defaults={
            'description': 'Relationship between education, experience, and income with non-linear patterns.',
            'source': 'Synthetic (World Bank style)',
            'features': ['education_years', 'experience_years'],
            'feature_descriptions': {
                'education_years': 'Years of formal education',
                'experience_years': 'Years of work experience',
            },
            'target': 'income',
            'units': 'USD/year',
            'data': df.to_dict('records'),
        }
    )
    
    print(f"  {'Created' if created else 'Updated'} dataset with {len(df)} samples")
    return dataset

def load_salary_dataset():
    """Create salary dataset with categorical features"""
    print("📊 Creating Salary Prediction dataset...")
    
    np.random.seed(42)
    n_samples = 800
    
    education = np.random.choice([0, 1, 2, 3, 4], n_samples)
    experience = np.random.uniform(0, 30, n_samples)
    sectors = np.random.choice(['Tech', 'Finance', 'Healthcare', 'Education'], n_samples)
    
    base = 30000
    salary = (base + 
             5000 * education ** 1.2 + 
             1000 * experience + 
             50 * experience ** 2)
    
    sector_mult = {'Tech': 1.5, 'Finance': 1.4, 'Healthcare': 1.2, 'Education': 0.9}
    for i, sector in enumerate(sectors):
        salary[i] *= sector_mult[sector]
    
    df = pd.DataFrame({
        'education_level': education,
        'experience': experience,
        'sector': sectors,
        'salary': salary
    })
    
    # One-hot encode for ML
    df_encoded = pd.get_dummies(df, columns=['sector'], prefix='sector')
    
    dataset, created = Dataset.objects.update_or_create(
        name='Salary Dataset',
        defaults={
            'description': 'Multi-sector salary data with categorical features.',
            'source': 'Synthetic (Kaggle style)',
            'features': [col for col in df_encoded.columns if col != 'salary'],
            'feature_descriptions': {
                'education_level': 'Education level (0: No degree, 1: Bachelor, 2: Master, 3: PhD, 4: Professional)',
                'experience': 'Years of experience',
                'sector_Tech': 'Tech sector (0/1)',
                'sector_Finance': 'Finance sector (0/1)',
                'sector_Healthcare': 'Healthcare sector (0/1)',
                'sector_Education': 'Education sector (0/1)',
            },
            'target': 'salary',
            'units': 'USD/year',
            'data': df_encoded.to_dict('records'),
        }
    )
    
    print(f"  {'Created' if created else 'Updated'} dataset with {len(df)} samples")
    return dataset

def load_all():
    """Load all datasets"""
    print("\n" + "="*50)
    print("📥 LOADING DATASETS INTO POSTGRESQL")
    print("="*50)
    
    load_boston_housing()
    load_education_dataset()
    load_salary_dataset()
    
    print("\n" + "="*50)
    print("✅ All datasets loaded successfully!")
    print(f"📊 Total datasets: {Dataset.objects.count()}")
    print("="*50)

if __name__ == '__main__':
    load_all()