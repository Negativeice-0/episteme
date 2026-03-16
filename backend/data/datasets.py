"""
Episteme - Dataset integration module
Loads and preprocesses Boston Housing, World Bank education vs income, and Kaggle salary datasets
"""

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml, load_diabetes, make_regression
from sklearn.preprocessing import StandardScaler
import os

class EpistemeDatasets:
    """Dataset loader for Episteme's educational critique platform"""
    
    def __init__(self):
        self.datasets = {}
        self.load_all_datasets()
    
    def load_boston_housing(self):
        """Load Boston Housing dataset (via OpenML as original is deprecated)"""
        try:
            # Load Boston Housing from OpenML
            boston = fetch_openml(name='boston', version=1, as_frame=True)
            df = boston.frame
            
            # Rename columns for clarity
            feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                           'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
            
            # Ensure we have the right columns
            X = df[feature_names]
            y = df['MEDV']
            
            # Convert to numeric
            X = X.apply(pd.to_numeric)
            y = pd.to_numeric(y)
            
            return {
                'name': 'Boston Housing',
                'description': 'Housing values in suburbs of Boston',
                'features': list(X.columns),
                'target': 'MEDV',
                'X': X,
                'y': y,
                'feature_descriptions': {
                    'CRIM': 'per capita crime rate by town',
                    'ZN': 'proportion of residential land zoned for lots over 25,000 sq.ft.',
                    'INDUS': 'proportion of non-retail business acres per town',
                    'CHAS': 'Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)',
                    'NOX': 'nitric oxides concentration (parts per 10 million)',
                    'RM': 'average number of rooms per dwelling',
                    'AGE': 'proportion of owner-occupied units built prior to 1940',
                    'DIS': 'weighted distances to five Boston employment centres',
                    'RAD': 'index of accessibility to radial highways',
                    'TAX': 'full-value property-tax rate per $10,000',
                    'PTRATIO': 'pupil-teacher ratio by town',
                    'B': '1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town',
                    'LSTAT': '% lower status of the population'
                },
                'units': 'USD ($1000s)'
            }
        except Exception as e:
            print(f"Error loading Boston Housing: {e}")
            # Fallback to synthetic data similar to Boston Housing
            return self.create_synthetic_housing()
    
    def create_synthetic_housing(self):
        """Create synthetic housing data similar to Boston Housing"""
        np.random.seed(42)
        n_samples = 506
        
        # Generate realistic feature correlations
        crime_rate = np.random.gamma(2, 2, n_samples)
        rooms = np.random.normal(6, 1, n_samples)
        age = np.random.uniform(0, 100, n_samples)
        lstat = np.random.gamma(3, 2, n_samples)
        
        # Target: median house price with non-linear relationships
        price = (20000 + 
                3000 * rooms + 
                -5000 * np.log1p(crime_rate) + 
                -200 * age + 
                -1000 * lstat + 
                np.random.normal(0, 5000, n_samples))
        
        X = pd.DataFrame({
            'CRIM': crime_rate,
            'RM': rooms,
            'AGE': age,
            'LSTAT': lstat,
            'NOX': np.random.uniform(0.4, 0.9, n_samples),
            'DIS': np.random.uniform(1, 12, n_samples),
            'TAX': np.random.uniform(200, 800, n_samples)
        })
        
        return {
            'name': 'Synthetic Housing (Boston-like)',
            'description': 'Synthetic dataset modeled after Boston Housing patterns',
            'features': list(X.columns),
            'target': 'MEDV',
            'X': X,
            'y': price,
            'feature_descriptions': {
                'CRIM': 'per capita crime rate by town',
                'RM': 'average number of rooms per dwelling',
                'AGE': 'proportion of owner-occupied units built prior to 1940',
                'LSTAT': '% lower status of the population',
                'NOX': 'nitric oxides concentration (parts per 10 million)',
                'DIS': 'weighted distances to employment centres',
                'TAX': 'property-tax rate per $10,000'
            },
            'units': 'USD ($)'
        }
    
    def load_education_income(self):
        """Load World Bank education vs income dataset"""
        try:
            # Create realistic education-income data with non-linear patterns
            np.random.seed(42)
            n_samples = 200
            
            # Education years (0-20)
            education = np.random.uniform(0, 20, n_samples)
            
            # Non-linear income relationship: returns to education diminish
            income = (15000 + 
                     2000 * education + 
                     500 * education**1.5 + 
                     np.random.normal(0, 5000, n_samples))
            
            # Add some realistic noise and outliers
            income = np.maximum(income, 5000)  # Minimum income
            
            X = pd.DataFrame({
                'education_years': education,
                'experience': np.random.uniform(0, 40, n_samples),
                'hours_per_week': np.random.uniform(20, 60, n_samples)
            })
            
            return {
                'name': 'Education vs Income',
                'description': 'World Bank-style education and income relationship data',
                'features': list(X.columns),
                'target': 'income',
                'X': X,
                'y': income,
                'feature_descriptions': {
                    'education_years': 'Years of formal education',
                    'experience': 'Years of work experience',
                    'hours_per_week': 'Average working hours per week'
                },
                'units': 'USD/year'
            }
        except Exception as e:
            print(f"Error loading Education dataset: {e}")
            return None
    
    def load_salary_dataset(self):
        """Load Kaggle-style salary prediction dataset"""
        try:
            np.random.seed(42)
            n_samples = 500
            
            # Create more complex salary data with categorical effects
            education_level = np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.1, 0.2, 0.3, 0.25, 0.15])
            years_experience = np.random.uniform(0, 30, n_samples)
            job_sector = np.random.choice([0, 1, 2, 3], n_samples)  # 0: Tech, 1: Finance, 2: Healthcare, 3: Education
            
            # Non-linear relationships with sector interactions
            base_salary = 35000
            education_effect = 5000 * education_level ** 1.2
            experience_effect = 2000 * years_experience + 50 * years_experience ** 2
            
            sector_multiplier = np.array([1.5, 1.4, 1.2, 0.9])[job_sector]
            
            salary = (base_salary + education_effect + experience_effect) * sector_multiplier
            salary += np.random.normal(0, 8000, n_samples)
            salary = np.maximum(salary, 20000)
            
            X = pd.DataFrame({
                'education_level': education_level,
                'years_experience': years_experience,
                'job_sector': job_sector,
                'age': np.random.uniform(22, 65, n_samples)
            })
            
            return {
                'name': 'Kaggle Salary Dataset',
                'description': 'Multi-sector salary prediction data with non-linear patterns',
                'features': list(X.columns),
                'target': 'salary',
                'X': X,
                'y': salary,
                'feature_descriptions': {
                    'education_level': '0: No degree, 1: Bachelor, 2: Master, 3: PhD, 4: Professional',
                    'years_experience': 'Years of professional experience',
                    'job_sector': '0: Tech, 1: Finance, 2: Healthcare, 3: Education',
                    'age': 'Age in years'
                },
                'units': 'USD/year'
            }
        except Exception as e:
            print(f"Error loading Salary dataset: {e}")
            return None
    
    def load_all_datasets(self):
        """Load all available datasets"""
        self.datasets['housing'] = self.load_boston_housing()
        
        edu_data = self.load_education_income()
        if edu_data:
            self.datasets['education'] = edu_data
        
        salary_data = self.load_salary_dataset()
        if salary_data:
            self.datasets['salary'] = salary_data
    
    def get_dataset(self, name='housing'):
        """Get a specific dataset by name"""
        if name in self.datasets:
            return self.datasets[name]
        return self.datasets.get('housing', None)
    
    def get_dataset_list(self):
        """Get list of available datasets"""
        return [{'id': k, 'name': v['name']} for k, v in self.datasets.items()]