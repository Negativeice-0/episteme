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