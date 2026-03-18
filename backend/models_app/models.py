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