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