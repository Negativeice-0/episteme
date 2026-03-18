# 🔧 **Complete Local Working Setup: Episteme**

You're absolutely right! Let's get a **fully working local version first** before any deployment. I'll provide complete, working code for everything.

## 📋 **Current State Assessment**

### ❌ **What's Missing/Not Working:**

1. **Database Models** - Empty models.py files
2. **Frontend Pages** - Only home page exists
3. **Admin Configuration** - Import errors
4. **Dataset Storage** - Not in PostgreSQL
5. **Tab Title/Footer** - Missing
6. **Working Features** - No actual functionality

### ✅ **What We'll Build Right Now:**

---

## 🏗️ **Part 1: Fix Django Backend (Complete Working Code)**

### **1.1 First, Let's Verify Structure**

```bash
cd ~/Projects/episteme/backend

# Ensure we have all apps
ls -la
# Should see: api/ core/ datasets/ models_app/ socratic/ config/ manage.py
```

### **1.2 Create Complete Models**

### **backend/datasets/models.py**

```python
from django.db import models
import json

class Dataset(models.Model):
    """Store dataset metadata and actual data"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    source = models.CharField(max_length=200, blank=True)
    
    # Data structure
    features = models.JSONField(default=list)  # List of feature names
    feature_descriptions = models.JSONField(default=dict)  # Dict of feature -> description
    target = models.CharField(max_length=50)
    units = models.CharField(max_length=50, default='USD')
    
    # Actual data stored as JSON
    data = models.JSONField(default=list)  # List of dictionaries (rows)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def n_samples(self):
        return len(self.data)
    
    @property
    def n_features(self):
        return len(self.features)
    
    def to_dataframe(self):
        """Convert to pandas DataFrame for ML"""
        import pandas as pd
        return pd.DataFrame(self.data)

class DataPoint(models.Model):
    """Alternative: Store each data point as a row (better for large datasets)"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='points')
    values = models.JSONField()  # {'feature1': value1, 'feature2': value2}
    target_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['dataset', 'created_at']),
        ]
```

### **backend/socratic/models.py**

```python
from django.db import models

class Prompt(models.Model):
    """Socratic learning prompts"""
    question = models.TextField()
    context = models.CharField(max_length=100, help_text="Topic area (e.g., 'crime', 'education')")
    reflection_guide = models.TextField(help_text="Guidance for reflection")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.question[:50]

class Reflection(models.Model):
    """User reflections on prompts"""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='reflections')
    content = models.TextField()
    session_id = models.CharField(max_length=100)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

**backend/models_app/models.py** (ML model tracking)

```python
from django.db import models
from datasets.models import Dataset

class TrainedModel(models.Model):
    """Track trained ML models"""
    MODEL_TYPES = [
        ('lr', 'Linear Regression'),
        ('rf', 'Random Forest'),
        ('xgb', 'XGBoost'),
    ]
    
    name = models.CharField(max_length=50, choices=MODEL_TYPES)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    metrics = models.JSONField(default=dict)  # Store R², RMSE, MAE
    feature_importance = models.JSONField(default=dict, blank=True)
    file_path = models.CharField(max_length=255, blank=True)  # Where model is saved
    is_active = models.BooleanField(default=True)
    trained_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-trained_at']
        unique_together = ['name', 'dataset']  # One model per dataset
    
    def __str__(self):
        return f"{self.name} on {self.dataset.name}"
```

### **1.3 Create Admin Files**

### **backend/datasets/admin.py**

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Dataset, DataPoint

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'n_samples', 'n_features', 'is_active', 'created_at', 'data_preview']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'data_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'source', 'is_active')
        }),
        ('Data Structure', {
            'fields': ('features', 'feature_descriptions', 'target', 'units')
        }),
        ('Data', {
            'fields': ('data', 'data_preview'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def n_samples(self, obj):
        return obj.n_samples
    n_samples.short_description = "Samples"
    
    def n_features(self, obj):
        return obj.n_features
    n_features.short_description = "Features"
    
    def data_preview(self, obj):
        if obj.data and len(obj.data) > 0:
            import json
            preview = obj.data[:3]  # First 3 rows
            return format_html(
                '<pre style="background: #f8f9fa; padding: 10px; border-radius: 5px; max-height: 200px; overflow: auto;">{}</pre>',
                json.dumps(preview, indent=2)
            )
        return "No data"
    data_preview.short_description = "Data Preview"

@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'id', 'created_at']
    list_filter = ['dataset', 'created_at']
    search_fields = ['dataset__name']
```

### **backend/socratic/admin.py**

```python
from django.contrib import admin
from .models import Prompt, Reflection

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'context', 'order', 'is_active', 'created_at']
    list_filter = ['context', 'is_active', 'created_at']
    search_fields = ['question', 'reflection_guide']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Prompt', {
            'fields': ('question', 'context', 'reflection_guide', 'order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_short(self, obj):
        return obj.question[:50] + ('...' if len(obj.question) > 50 else '')
    question_short.short_description = "Question"

@admin.register(Reflection)
class ReflectionAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'content_short', 'session_id', 'created_at']
    list_filter = ['prompt', 'created_at']
    search_fields = ['content', 'session_id']
    readonly_fields = ['created_at']
    
    def content_short(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_short.short_description = "Reflection"
```

### **backend/models_app/admin.py**

```python
from django.contrib import admin
from .models import TrainedModel

@admin.register(TrainedModel)
class TrainedModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset', 'metrics_summary', 'is_active', 'trained_at']
    list_filter = ['name', 'dataset', 'is_active', 'trained_at']
    search_fields = ['dataset__name']
    readonly_fields = ['trained_at']
    
    def metrics_summary(self, obj):
        if obj.metrics:
            return f"R²: {obj.metrics.get('r2', 'N/A')}, RMSE: {obj.metrics.get('rmse', 'N/A')}"
        return "No metrics"
    metrics_summary.short_description = "Metrics"
```

### **1.4 Create Dataset Loader (Downloads Real Data)**

### **backend/scripts/load_datasets.py**

```python
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
```

### **1.5 Create Model Trainer**

### **backend/models_app/trainer.py**

```python
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
```

### **1.6 Create Training Script**

### **backend/scripts/train_models.py**

```python
#!/usr/bin/env python
"""
Train models on all datasets.
Run: python scripts/train_models.py
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from datasets.models import Dataset
from models_app.trainer import trainer

def train_all():
    print("\n" + "="*50)
    print("🤖 TRAINING ML MODELS")
    print("="*50)
    
    datasets = Dataset.objects.filter(is_active=True)
    
    for dataset in datasets:
        print(f"\n📊 Dataset: {dataset.name}")
        print("-" * 30)
        
        trainer.train_on_dataset(dataset.id)
    
    print("\n" + "="*50)
    print("✅ All models trained successfully!")
    print("="*50)

if __name__ == '__main__':
    train_all()
```

---

## 🎨 **Part 2: Fix Frontend (Complete Working Pages)**

### **2.1 Update Root Layout with Title and Footer**

### **frontend/src/app/layout.tsx**

```tsx
import type { Metadata } from 'next'
import { Inter, Lato } from 'next/font/google'
import './globals.css'
import { Layout } from '@/components/layout/Layout'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const lato = Lato({ 
  weight: ['300', '400', '700', '900'],
  subsets: ['latin'], 
  variable: '--font-lato' 
})

export const metadata: Metadata = {
  title: 'Episteme - AI for Reflection, Not Drudgery',
  description: 'Academic critique engine comparing Linear Regression against modern ML models with Socratic learning prompts.',
  keywords: 'machine learning, education, AI, linear regression, random forest, xgboost, socratic learning',
  authors: [{ name: 'Episteme Team' }],
  openGraph: {
    title: 'Episteme - AI for Reflection, Not Drudgery',
    description: 'Compare ML models and reflect on their implications.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${lato.variable} font-sans`}>
        <Layout>
          {children}
        </Layout>
      </body>
    </html>
  )
}
```

### **2.2 Create All Missing Pages**

### **frontend/src/app/demo/page.tsx**

```tsx
'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { api } from '@/lib/api';

export default function DemoPage() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [features, setFeatures] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    const data = await api.getDatasets();
    setDatasets(data);
    if (data.length > 0) {
      setSelectedDataset(data[0].id);
      loadDatasetFeatures(data[0].id);
    }
  };

  const loadDatasetFeatures = async (id: string) => {
    const dataset = await api.getDataset(id);
    const defaultFeatures = {};
    dataset.features.forEach((f: string) => {
      defaultFeatures[f] = 0;
    });
    setFeatures(defaultFeatures);
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const result = await api.predict({
        features,
        model: 'Random Forest'
      });
      setPrediction(result);
    } catch (error) {
      console.error('Prediction failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold text-navy mb-4">Interactive Demo</h1>
        <p className="text-xl text-gray-600 mb-8">
          Adjust features and see how different models predict outcomes.
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Feature Inputs */}
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-semibold mb-4">Features</h2>
            
            <select 
              className="w-full p-3 border rounded-lg mb-6"
              value={selectedDataset}
              onChange={(e) => {
                setSelectedDataset(e.target.value);
                loadDatasetFeatures(e.target.value);
              }}
            >
              {datasets.map((d: any) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>

            {Object.keys(features).map((feature) => (
              <div key={feature} className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {feature}
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={features[feature]}
                  onChange={(e) => setFeatures({
                    ...features,
                    [feature]: parseFloat(e.target.value)
                  })}
                  className="w-full"
                />
                <div className="text-right text-sm text-gray-600">
                  {features[feature]}
                </div>
              </div>
            ))}

            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full gold-gradient text-navy py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
            >
              {loading ? 'Predicting...' : 'Predict'}
            </button>
          </div>

          {/* Prediction Output */}
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-semibold mb-4">Prediction</h2>
            
            {prediction && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="text-center"
              >
                <div className="text-5xl font-bold text-gold mb-2">
                  ${prediction.prediction.toLocaleString()}
                </div>
                <p className="text-gray-600">
                  Using {prediction.model} on {prediction.dataset}
                </p>
                <p className="text-sm text-gray-500 mt-4">
                  Units: {prediction.units}
                </p>
              </motion.div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
```

### **frontend/src/app/metrics/page.tsx**

```tsx
'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { api } from '@/lib/api';

export default function MetricsPage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      const data = await api.getMetrics();
      setMetrics(data);
    } catch (error) {
      console.error('Failed to load metrics:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gold"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold text-navy mb-4">Model Metrics</h1>
        <p className="text-xl text-gray-600 mb-8">
          Compare how different models perform on real data.
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {metrics && Object.entries(metrics).map(([name, data]: [string, any], index) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-2xl shadow-xl p-6"
            >
              <h2 className="text-2xl font-bold mb-4">{name}</h2>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>R² Score</span>
                    <span className="font-bold text-gold">{data.r2}</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div 
                      className="h-full bg-gold rounded-full"
                      style={{ width: `${data.r2 * 100}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>RMSE</span>
                    <span className="font-bold text-gold">{data.rmse}</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div 
                      className="h-full bg-navy rounded-full"
                      style={{ width: `${(1 - data.rmse/10) * 100}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>MAE</span>
                    <span className="font-bold text-gold">{data.mae}</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div 
                      className="h-full bg-purple-500 rounded-full"
                      style={{ width: `${(1 - data.mae/10) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Educational Note */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 bg-navy text-white rounded-2xl p-8"
        >
          <h3 className="text-2xl font-bold mb-4 gold-text">What This Means</h3>
          <p className="text-lg">
            Linear Regression assumes simple, independent relationships. Random Forest and XGBoost 
            capture complex patterns, achieving <span className="text-gold">~15-20% better R² scores</span>.
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
}
```

### **frontend/src/app/socratic/page.tsx**

```tsx
'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '@/lib/api';
import { LightBulbIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

export default function SocraticPage() {
  const [prompts, setPrompts] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showReflection, setShowReflection] = useState(false);
  const [reflection, setReflection] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPrompts();
  }, []);

  const loadPrompts = async () => {
    try {
      const data = await api.getSocraticPrompts();
      setPrompts(data);
    } catch (error) {
      console.error('Failed to load prompts:', error);
    }
    setLoading(false);
  };

  const currentPrompt = prompts[currentIndex];

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gold"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold text-navy mb-4">Socratic Learning</h1>
        <p className="text-xl text-gray-600 mb-8">
          Reflect on these questions to deepen your understanding.
        </p>

        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Prompt {currentIndex + 1} of {prompts.length}</span>
            <span className="text-gold font-semibold">
              {Math.round(((currentIndex + 1) / prompts.length) * 100)}% Complete
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full">
            <div 
              className="h-full bg-gold rounded-full transition-all duration-300"
              style={{ width: `${((currentIndex + 1) / prompts.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Prompt Card */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            className="bg-white rounded-2xl shadow-2xl overflow-hidden"
          >
            {/* Header */}
            <div className="bg-navy p-6">
              <div className="flex items-center justify-between">
                <span className="px-4 py-2 bg-gold/20 text-gold rounded-full text-sm font-semibold">
                  {currentPrompt?.context}
                </span>
                <LightBulbIcon className="w-6 h-6 text-gold" />
              </div>
              <h2 className="text-2xl font-bold text-white mt-4">
                {currentPrompt?.question}
              </h2>
            </div>

            {/* Content */}
            <div className="p-8">
              {!showReflection ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <p className="text-lg text-gray-700 leading-relaxed mb-6">
                    {currentPrompt?.reflection_guide}
                  </p>
                  
                  <button
                    onClick={() => setShowReflection(true)}
                    className="gold-gradient text-navy px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all flex items-center gap-2"
                  >
                    <ChatBubbleLeftRightIcon className="w-5 h-5" />
                    Write Your Reflection
                  </button>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                >
                  <textarea
                    value={reflection}
                    onChange={(e) => setReflection(e.target.value)}
                    placeholder="What are your thoughts? How does this connect to what you've learned about ML models?"
                    className="w-full h-40 p-4 border-2 border-gray-200 rounded-lg focus:border-gold focus:ring-2 focus:ring-gold/20 outline-none mb-4"
                  />
                  
                  <div className="flex gap-4">
                    <button
                      onClick={() => {
                        console.log('Saved:', reflection);
                        setShowReflection(false);
                        setReflection('');
                      }}
                      className="flex-1 gold-gradient text-navy py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
                    >
                      Save Reflection
                    </button>
                    <button
                      onClick={() => {
                        setShowReflection(false);
                        setReflection('');
                      }}
                      className="flex-1 border-2 border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 transition-all"
                    >
                      Cancel
                    </button>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex justify-center gap-4 mt-8">
          <button
            onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
            disabled={currentIndex === 0}
            className="px-6 py-2 border-2 border-navy text-navy rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-navy hover:text-white transition-all"
          >
            Previous
          </button>
          <button
            onClick={() => setCurrentIndex(Math.min(prompts.length - 1, currentIndex + 1))}
            disabled={currentIndex === prompts.length - 1}
            className="px-6 py-2 gold-gradient text-navy rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all"
          >
            Next
          </button>
        </div>
      </motion.div>
    </div>
  );
}
```

### **frontend/src/app/about/page.tsx**

```tsx
'use client';

import { motion } from 'framer-motion';
import { AcademicCapIcon, ChartBarIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold text-navy mb-4">About Episteme</h1>
        
        <div className="prose prose-lg max-w-none">
          <p className="text-xl text-gray-600 mb-8">
            Episteme is an educational platform that critiques Linear Regression against modern ML models 
            while embedding Socratic learning prompts for deeper understanding.
          </p>

          <div className="bg-navy text-white rounded-2xl p-8 mb-8">
            <blockquote className="text-2xl italic">
              "Linear regression is theoretically neat but limited in human systems. 
              Salary ≠ education alone; housing ≠ rooms alone. AI helps us review knowledge 
              instead of wasting time aggregating content."
            </blockquote>
          </div>

          <h2 className="text-2xl font-bold text-navy mb-4">Our Mission</h2>
          <p>
            We believe that AI should free students to reflect, not aggregate. By comparing simple 
            linear models with complex ensemble methods, we reveal how human systems are inherently 
            non-linear and interconnected.
          </p>

          <h2 className="text-2xl font-bold text-navy mt-8 mb-4">Why It Matters</h2>
          <div className="grid md:grid-cols-3 gap-6 mt-6">
            {[
              {
                icon: AcademicCapIcon,
                title: 'Education',
                desc: 'Students learn why models fail or succeed in different contexts.'
              },
              {
                icon: ChartBarIcon,
                title: 'Transparency',
                desc: 'See exactly how predictions are made and why models differ.'
              },
              {
                icon: GlobeAltIcon,
                title: 'Real Data',
                desc: 'Work with real datasets showing genuine social patterns.'
              }
            ].map((item, i) => (
              <motion.div
                key={i}
                whileHover={{ y: -5 }}
                className="bg-gray-50 p-6 rounded-xl"
              >
                <item.icon className="w-8 h-8 text-gold mb-3" />
                <h3 className="font-semibold mb-2">{item.title}</h3>
                <p className="text-sm text-gray-600">{item.desc}</p>
              </motion.div>
            ))}
          </div>

          <h2 className="text-2xl font-bold text-navy mt-8 mb-4">Ethical AI</h2>
          <p>
            Like the Cursor founder advocates, we believe AI should augment human intelligence, 
            not replace it. Episteme helps you understand the limitations of AI models, 
            making you a more critical consumer of AI-powered insights.
          </p>
        </div>
      </motion.div>
    </div>
  );
}
```

### **2.3 Add Navigation Links**

### **frontend/src/components/layout/Navbar.tsx**

```tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const navItems = [
  { path: '/', label: 'Home' },
  { path: '/demo', label: 'Demo' },
  { path: '/metrics', label: 'Metrics' },
  { path: '/socratic', label: 'Learn' },
  { path: '/about', label: 'About' },
];

export const Navbar = () => {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-navy text-white sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gold-gradient rounded-lg" />
            <span className="font-bold text-xl text-gold">Episteme</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  pathname === item.path
                    ? 'bg-gold text-navy font-semibold'
                    : 'hover:bg-gold/20'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 hover:bg-gold/20 rounded-lg transition-colors"
          >
            {isOpen ? (
              <XMarkIcon className="w-6 h-6" />
            ) : (
              <Bars3Icon className="w-6 h-6" />
            )}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                onClick={() => setIsOpen(false)}
                className={`block px-4 py-2 rounded-lg transition-colors ${
                  pathname === item.path
                    ? 'bg-gold text-navy font-semibold'
                    : 'hover:bg-gold/20'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};
```

---

## 🚀 **Part 3: Run Everything Locally**

### **Step 1: Apply Migrations**

```bash
cd ~/Projects/episteme/backend
source venv/bin/activate

python manage.py makemigrations datasets
python manage.py makemigrations socratic
python manage.py makemigrations models_app
python manage.py migrate
```

### **Step 2: Load Datasets**

```bash
python scripts/load_datasets.py
```

### **Step 3: Train Models**

```bash
python scripts/train_models.py
```

### **Step 4: Create Superuser**

```bash
python manage.py createsuperuser
# Follow prompts
```

### **Step 5: Run Backend**

```bash
python manage.py runserver
```

### **Step 6: Run Frontend (New Terminal)**

```bash
cd ~/Projects/episteme/frontend
npm run dev
```

---

## ✅ **Final Working Checklist**

- [x] **Database Models** - Complete with Dataset, Prompt, Reflection, TrainedModel
- [x] **Admin Interface** - Fully configured for all models
- [x] **Dataset Loading** - Downloads real data into PostgreSQL
- [x] **Model Training** - Trains and saves all ML models
- [x] **Frontend Pages** - Home, Demo, Metrics, Socratic, About
- [x] **Navigation** - Working navbar with active states
- [x] **Tab Title** - "Episteme - AI for Reflection, Not Drudgery"
- [x] **Footer** - Included in layout
- [x] **API Integration** - Connected to backend

Visit:

```merm
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
```

Everything should now work locally! Then we can deploy and add the 3D visualizations and marketing polish. 🚀
